// Copyright (c) 2017-2021, Mudita Sp. z.o.o. All rights reserved.
// For licensing, see https://github.com/mudita/MuditaOS/LICENSE.md

#pragma once
#include <tuple>
#include <cstdint>
#include <memory>

namespace audio {
    namespace detail {
        struct DecoderResamplerImpl;
    };
    class DecoderResampler
    {
    public:
        DecoderResampler( DecoderResampler& ) = delete;
        DecoderResampler& operator=(DecoderResampler&) = delete;

        DecoderResampler();
        ~DecoderResampler();

        /** Initalize and configure resampler to the output rate
         * @param[in] inputRate Input sample rate
         * @param[in] outputRate Output sample rate
         * @param[in] nChann Number of channels
         * @param[in] Maximum number of samples in buf
         * @return Configuration error code
         */
        int configure(uint32_t inputRate, uint32_t outputRate, uint8_t nChann, std::size_t samplesChunk);
        /** Resample stream to the output format
         * @param[in] samplesToRead Numer of samples to read
         * @param[in] pcmData Input PCM data
         * @return output buffer and buffer size
         */
        std::tuple<int16_t*,std::size_t> operator()(uint32_t samplesToRead, int16_t* pcmData);

    private:
        std::unique_ptr<detail::DecoderResamplerImpl> impl;
        std::unique_ptr<int16_t[]> outBuf {};
        std::size_t origBufLen {};
        std::size_t bufLen {};
        uint8_t nChannels {};
        uint32_t mOutputRate {};
        uint32_t mInputRate {};
    };
}
