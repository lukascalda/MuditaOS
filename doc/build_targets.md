# Products

In one source tree we have two products, short names in brackets:

* PurePhone ( Pure )
* BellHybrid ( Bell )

For simplicity, we have defined a few CMake targets that will create required images and update packages.

# Architectures

We support two target architectures:

* Linux x86_64
* RT1051

Some build targets are enabled/disabled based on the selected target architecture.

# Targets

For each product there are targets:


| Arch | Name | Alias | Description |
|------|------|-------|-------------|
|common| \<Product\>                    |                                                   | Binary target for the product |
|common| \<Product\>-disk-img           | \<Product\>.img                                   | Disk image for the product    |
|RT1051| \<Product\>-StandaloneImage    | PurePhone-\<version\>-RT1051-package-standalone   | Creates image that can be `dd` or `pureflash` to the device|
|RT1051| \<Product>\-UpdatePackage      | PurePhone-\<version\>-RT1051-Update.tar           | Creates Update package, that can be used by Mudita Center or an update script|
|linux | check                          |                                                   | build and run unittests |
|common| assets                         |                                                   | Mudita company private assets |
|common| json-images-target             |                                                   | Mudita company public assets |
|RT1051| ecoboot.bin                    |                                                   | OS bootloader |
|RT1051| updater.bin                    |                                                   | OS updater |

## Product binary target

The software binary can be loaded by:
- JLink
- Directly onto the device by:
    - Updater utility
    - direct memory access

Devices in the field have security keys burned, therefore an additional step - binary signing will be required. Without the signature, devices will show a warning on boot.

## Disk image

Image of the software to be loaded onto the device memory. Has all necessary data to properly run the OS. 
The disk image can be built with additional, development assets. Please look for `WITH_DEVELOPMENT_FEATURES` for more information in make.

## Update package

Tar-file meant to update software with the updater utility. It has all the necessary update assets and metadata.
Currently, the update package has all of the base data that should be on the device, though to make updates smaller, minimal updates packages, as well as gzipped packages should be easily possible.

## Check

Builds and executes all of the unit tests in the repository for the selected product.
Uses [download_assets](./download_assets.md) to download unit test's required assets (fonts)

## assets

Downloads Mudita private assets with [download_assets](./download_assets.md) that company is either not eligible or capable of sharing publicly.
These are distributed with the image and update targets available for each product and. includes i.e. fonts.

## json-images-target

Downloads Mudita public assets with [download_assets](./download_assets.md).

## ecoboot.bin

Downloads the bootloader with [download_assets](./download_assets.md).

OS bootloader, used to pre-init hardware and launch either OS or updater utility.

## updater.bin

Downloads the updater with [download_assets](./download_assets.md).

Updater is used to perform the firmware upgrade via update packages. 
