[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

<!--
<a href="https://singularitynet.io/">
<img align="right" src="../assets/logo/singularityNETblue.png" alt="drawing" width="160"/>
</a>
-->

# Super Resolution

This service uses convolutional neural networks to increase the resolution of an image by reconstructing rather than simply resizing it.

It is part of SingularityNET's third party services, [originally implemented by fperazzi](https://github.com/fperazzi/proSR).

### Welcome

The service takes an image as input passes it through to a pre-trained deep neural network model that increases its original resolution.

There are two types of pre-trained models available: proSR and proSRGAN (proSR trained with adversarial loss). According to the authors, proSRGAN generates lower PSNR (peak signal to noise ratio) but higher details. 

The image resolution can be increased by a scale of 2, 4 or 8 when using proSR models or by 4 or 8 using proSRGAN models.

### What’s the point?

If an image of interest is too small for a given application, this service can be used to upscale the original image producing more detail-realistic (less blurry) outputs than simply resizing it.

### How does it work?

The user must provide the following inputs in order to start the service and get a response:

Inputs:
  - `input`: The URL for a .jpg or .png input image.
  - `model`: Can be either "proSR" or "proSRGAN".
  - `scale`: The upscaling factor as an integer. Can take values \[2, 4 or 8\] for "proSR" models or \[4 or 8\] for "proSRGAN" models.
Outputs:
  - `output_image`: A base64 encoded image that has the same extension of the input image.

You can use this service at [SingularityNET DApp](http://alpha.singularitynet.io/) by clicking on `snet/super-resolution`.

You can also call the service from SingularityNET CLI (`snet`). Assuming that you have an open channel (`id: 0`) to this service:

```
$ snet client call 0 0 54.203.198.53:7017 increase_image_resolution '{"input": "https://www.gettyimages.ie/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg", "model": "proSR", "scale": 2}'
```

Go to [this tutorial](https://github.com/singnet/wiki/tree/master/tutorials/howToPublishService) to learn more about publishing, using and deleting a service.

### What to expect from this service?

Example:

- Model: "proSR"
- Scale: 2
- Input image:

![Tiger](assets/users_guide/tiger_original.jpeg)

- Output image:

![Tiger_proSR_2](assets/users_guide/tiger_proSR_2.jpeg)

Comparison:

Service Output (proSR)             | Simple Bicubic Upscaling
:---------------------------------:|:-------------------------:
<img src="assets/users_guide/tiger_proSR_2.jpeg"> | <img src="assets/users_guide/tiger_bicubic.jpeg">
