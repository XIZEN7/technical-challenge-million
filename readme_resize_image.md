# Technical Challenge Million
### Image Processing with Cloudflare

#### Description
The code allows fetching and processing an image from a URL specified in the environment variables using Cloudflare for image handling and resizing.

#### Diagram
![million_up drawio](https://github.com/XIZEN7/technical-challenge-million/assets/60405554/91006d4c-9f47-4a4e-911c-fbd60b48df37)

#### Requirements
- Node.js with support for `async/await`.
- The `dotenv` package to load environment variables from a `.env` file.

#### Configuration
1. Ensure you have a `.env` file in the root of the project with the following variable:
   ```
   IMAGE_URL_CLOUDFLARE=<image_url>
   ```
   Where `<image_url>` is the URL of the image to be processed.

#### Variables
- `targetWidth`: Desired width for the processed image (720 pixels).
- `targetHeight`: Desired height for the processed image (1080 pixels).
- `IMAGE_URL_CLOUDFLARE`: URL of the image obtained from the environment variables.

#### Processing Options
The code uses the following options for image processing:
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
```
- `width`: Target width of the image.
- `height`: Target height of the image.
- `fit`: Image fitting method (in this case, 'scale-down').
- `format`: Image format (in this case, 'auto').

#### Main Function
The `fetchAndProcessImage` function performs the following steps:
1. Checks if the image URL is defined in the environment variables.
2. Validates that the image format is one of the allowed formats (PNG, JPEG, JPG, SVG).
3. Fetches the image from the specified URL with the resizing options.
4. Checks if the image download was successful.
5. Compares the original image dimensions with the desired dimensions.
6. Returns a message indicating the status of the image processing.

#### Error Handling
- If any error occurs during the image fetching or processing, it is caught and logged to the console.
- Returns an error message with HTTP status 500 if any issue arises.

#### Execution
To run the code, make sure you have the environment variables configured correctly, then call the `fetchAndProcessImage(options)` function. This function returns a promise that you can handle to get the result of the image processing.

