# Image Fetch and Process

This repository contains a JavaScript function `fetchAndProcessImage` that fetches an image from a specified URL, processes it with Cloudflare's image resizing service, and checks the dimensions against target dimensions.

## Diagram
![million_up drawio](https://github.com/XIZEN7/technical-challenge-million/assets/60405554/91006d4c-9f47-4a4e-911c-fbd60b48df37)

## Usage

To use the `fetchAndProcessImage` function:

1. Replace `URL_OF_YOUR_IMAGE_HERE` in the `imageUrl` variable with the URL of the image you want to process.

2. Customize the `options` object in the `const options` section according to your image processing requirements. Currently, it resizes the image to `targetWidth` x `targetHeight` pixels using Cloudflare's image resizing service.

3. Run the script and check the console for the result message.

## Function Explanation

The `fetchAndProcessImage` function does the following:

- **Fetches the Image**: Fetches the image from the specified URL using the `fetch` API with provided options.

- **Checks Response**: Checks if fetching the image was successful (`response.ok`). If not, throws an error.

- **Checks Resized Image Dimensions**: Retrieves the dimensions of the resized image from the response header (`cf-image-dimensions`).

- **Compares Dimensions**: Compares the original dimensions of the image with the target dimensions (`targetWidth` x `targetHeight`) and prepares a message based on the comparison.

- **Returns Response**: Returns a `Response` object with a message indicating the status of the image dimensions.

- **Error Handling**: Catches and handles errors that occur during fetching or processing, logging them to the console and returning an appropriate error response.

## Example

```javascript
const options = {
    cf: {
        image: {
            width: targetWidth,
            height: targetHeight,
            fit: 'scale-down',
            format: 'auto'
        }
    }
};

const imageUrl = 'URL_OF_YOUR_IMAGE_HERE';

fetchAndProcessImage(imageUrl, options)
    .then(response => {
        console.log(response);
    })
    .catch(error => {
        console.error('Error processing image:', error);
    });
```

## Requirements

- Node.js environment
- Properly configured Cloudflare account for image resizing
