cmake_minimum_required(VERSION 3.13)
add_library(fresample STATIC)
add_library(fresample::fresample ALIAS fresample)


target_include_directories(fresample
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src/include>
)

target_sources(fresample
    PRIVATE
        src/lib/cpu.c
        src/lib/filter_delay.c
        src/lib/filter_free.c
        src/lib/filter_get.c
        src/lib/filter_new.c
        src/lib/filter_new_window.c
        src/lib/info_name.c
        src/lib/param.c
        src/lib/param_name.c
        src/lib/resample.c
        src/lib/resample_s16func.c
        src/lib/resample_s16n1f32_scalar.c
        src/lib/resample_s16n1s16_scalar.c
        src/lib/resample_s16n2f32_scalar.c
        src/lib/resample_s16n2s16_scalar.c
        src/lib/swap16.c
        src/lib/swap16_scalar.c
    PRIVATE
        src/lib/convert.h
        src/lib/cpu.h
        src/lib/filter.h
        src/lib/resample.h
)
