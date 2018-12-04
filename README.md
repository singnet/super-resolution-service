[issue-template]: ../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../issues/new?template=FEATURE_REQUEST.md

<a href="https://singularitynet.io/">
<img align="right" src="./docs/assets/logo/singularityNETblue.png" alt="drawing" width="160"/>
</a>

# Super Resolution

> Repository for the super resolution service on the SingularityNET.

[![Github Issues](https://img.shields.io/github/issues-raw/singnet/super-resolution-service.svg?style=popover)](https://github.com/singnet/super-resolution-service/issues)
[![Pending Pull-Requests](https://img.shields.io/github/issues-pr-raw/singnet/super-resolution-service.svg?style=popover)](https://github.com/singnet/super-resolution-service/pulls)
[![GitHub License](	https://img.shields.io/github/license/singnet/dnn-model-services.svg?style=popover)](https://github.com/singnet/super-resolution-service/blob/master/LICENSE)
[![CircleCI](https://circleci.com/gh/singnet/super-resolution-service.svg?style=svg)](https://circleci.com/gh/singnet/super-resolution-service)

This service uses convolutional neural networks to increase the resolution of an image by reconstructing rather than simply resizing it. It can upscale images by a factor of 2, 4 or 8.

This repository was forked from [fperazzi/proSR](https://github.com/fperazzi/proSR). The original code is written in Python 3 (using Pytorch) and has been integrated into the SingularityNET using Python 3.6.

Refer to:
- [The User's Guide](https://singnet.github.io/super-resolution-service/): for information about how to use this code as a SingularityNET service;
- [The Original Repository](https://github.com/fperazzi/proSR): for up-to-date information on [FPerazzi](https://github.com/fperazzi) implementation of this code.
- [SingularityNET Wiki](https://github.com/singnet/wiki): for information and tutorials on how to use the SingularityNET and its services.

## Contributing and Reporting Issues

Please read our [guidelines](https://github.com/singnet/wiki/blob/master/guidelines/CONTRIBUTING.md#submitting-an-issue) before submitting an issue. If your issue is a bug, please use the bug template pre-populated [here][issue-template]. For feature requests and queries you can use [this template][feature-template].

## Authors

* **Ramon Durães** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)

## Licenses

This project is licensed under the MIT License. The original repository is licensed under the GNU General Public License. See the [LICENSE](LICENSE) file for details. 