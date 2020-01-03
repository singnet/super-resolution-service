[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

<!--
<a href="https://singularitynet.io/">
<img align="right" src="../assets/logo/singularityNETblue.png" alt="drawing" width="160"/>
</a>
-->

# Super Resolution

This service uses convolutional neural networks to increase the resolution of an image by reconstructing rather than simply resizing it.

It is part of SingularityNET's third party services, [originally implemented by xinntao](https://github.com/xinntao/ESRGAN).

### Welcome

The service takes an image as input passes it through to a pre-trained deep neural network model that increases its original resolution.

The pre-trained model made available in this service is called "ESRGAN" and upscales images by a factor of 4. It won the first place in PIRM2018-SR competition (region 3) and got the best perceptual index. 

### What’s the point?

If an image of interest is too small for a given application, this service can be used to upscale the original image producing more detail-realistic (less blurry) outputs than simply resizing it.

### How does it work?

The user must provide the following inputs in order to start the service and get a response:

Inputs:
  - `input`: The URL for the input image. **Please note that while .jpg and .png image formats are both accepted, results are better on .png images. JPEG compression generates "blocky" artifacts that are emphasized on the output, generating suboptimal results.** 
  - `model`: The pre-trained mode. Should be "ESRGAN". This field takes only one model option but was kept in case different models are added to the service.
  - `scale`: The upscaling factor as an integer. Should be 4. This field takes only one scale option but was kept in case different models are added to the service.
Outputs:
  - `output_image`: A base64 encoded image that has the same extension of the input image.

You can use this service at [SingularityNET DApp](http://beta.singularitynet.io/) by clicking on `snet/super-resolution`.

You can also call the service from SingularityNET CLI (`snet`). Assuming that you have an open channel (`id: 269`) to this service:

```
$ snet client call snet super-resolution increase_image_resolution '{"input": "https://www.gettyimages.ie/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg", "model": "ESRGAN", "scale": 4}'
```

Go to [this tutorial](https://github.com/singnet/wiki/tree/master/tutorials/howToPublishService) to learn more about publishing, using and deleting a service.

### What to expect from this service?

Example:

- Model: "ESRGAN"
- Scale: 4
- Input image:

![Baboon](assets/users_guide/baboon.png)

- Output image:

![Baboon_ESRGANx4](assets/users_guide/baboon_rlt.png)

Comparison:

Service Output (ESRGAN)             | Simple Bicubic Upscaling
:---------------------------------:|:-------------------------:
<img src="assets/users_guide/baboon_rlt.png"> | <img src="assets/users_guide/baboon_bicubic.png">
