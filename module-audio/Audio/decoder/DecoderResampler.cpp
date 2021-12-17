// Copyright (c) 2017-2021, Mudita Sp. z.o.o. All rights reserved.
// For licensing, see https://github.com/mudita/MuditaOS/LICENSE.md


#include "DecoderResampler.hpp"
#include <fresample.h>
#include <memory>
#include <cmath>
#include <log/log.hpp>

namespace audio {
    namespace detail {
        struct DecoderResamplerImpl {
            struct lfr_param* param {};
            lfr_fixed_t inv_ratio {};
            lfr_fixed_t pos {};
            lfr_fixed_t pos0 {};
            struct lfr_filter *fp {};
            unsigned dither {};
            ~DecoderResamplerImpl() {
                if(fp) {
                    lfr_param_free(param);
                    lfr_filter_free(fp);
                }
            }
        };
    };

    namespace {
      constexpr auto DITHER_SEED = 0xc90fdaa2U;
    }

    DecoderResampler::DecoderResampler()
        : impl(std::make_unique<detail::DecoderResamplerImpl>())
    {
    }

    DecoderResampler::~DecoderResampler()
    {
    }

    // Prepare resampler
    int DecoderResampler::configure(uint32_t inputRate, uint32_t outputRate, uint8_t nChann, std::size_t samplesChunk)
    {
        bufLen = std::floor(
            double(samplesChunk) * double(outputRate) / double(inputRate) + 0.5);
        outBuf = std::make_unique<int16_t[]>(bufLen);
        LOG_INFO("Resample configure inputSR: %u outputSR: %u nchn: %u maxLen: %u",
                unsigned(inputRate), unsigned(outputRate), unsigned(nChann), unsigned(samplesChunk) );
        impl->inv_ratio =  (((lfr_fixed_t) outputRate << 32) + inputRate / 2) / outputRate;
        if(impl->param) {
            lfr_param_free(impl->param);
        }
        impl->param = lfr_param_new();

        lfr_param_seti(impl->param, LFR_PARAM_INRATE, inputRate);
        lfr_param_seti(impl->param, LFR_PARAM_OUTRATE, outputRate);
        if(impl->fp) {
            lfr_filter_free(impl->fp);
        }
        lfr_filter_new(&impl->fp, impl->param);
        if (!impl->fp) {
            LOG_ERROR("Unable to allocate filter");
            return -1;
        }
        impl->pos0 = -lfr_filter_delay(impl->fp);
        impl->pos = impl->pos0;
        impl->dither = DITHER_SEED;
        nChannels = nChann;
        origBufLen = samplesChunk;
        mOutputRate = outputRate;
        mInputRate = inputRate;
        return 0;
    }

    // Make resample
    std::tuple<int16_t*,std::size_t> DecoderResampler::operator()(uint32_t samplesToRead, int16_t* pcmData)
    {
        if(samplesToRead==0) {
            return { outBuf.get(), 0 };
        }
        std::size_t outlen = (samplesToRead==origBufLen)?bufLen:(
                std::floor( double(samplesToRead) * double(mOutputRate) / double(mInputRate) + 0.5));
        lfr_resample( &impl->pos, impl->inv_ratio, &impl->dither, nChannels,
                outBuf.get(), LFR_FMT_S16LE, outlen,
                pcmData, LFR_FMT_S16LE, samplesToRead,
                impl->fp
        );
        return { outBuf.get(), outlen };
    }
}
