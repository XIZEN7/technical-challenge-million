require('dotenv').config(); // Load environment variables from .env

const targetWidth = 720;
const targetHeight = 1080;

const IMAGE_URL_CLOUDFLARE = process.env.IMAGE_URL_CLOUDFLARE;

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

async function fetchAndProcessImage(options) {
    try {
        if (!IMAGE_URL_CLOUDFLARE) {
            throw new Error('Image URL not found in environment variables.');
        }

        // Validate allowed formats
        const allowedFormats = ['image/png', 'image/jpeg', 'image/jpg', 'image/svg+xml'];

        // Get image format extension from URL
        const extension = IMAGE_URL_CLOUDFLARE.split('.').pop();
        const contentType = `image/${extension}`;

        if (!allowedFormats.includes(contentType)) {
            throw new Error(`Image format (${contentType}) is not supported. Expected: PNG, JPEG, JPG, SVG.`);
        }

        // Fetch the image with specified options
        const response = await fetch(IMAGE_URL_CLOUDFLARE, options);

        // Check if fetching the image was successful
        if (!response.ok) {
            throw new Error(`Failed to fetch image: ${response.statusText}`);
        }

        // Get the resized image dimensions header
        const resizedImageSize = response.headers.get('cf-image-dimensions');

        let message = '';

        // Check if resizedImageSize exists
        if (!resizedImageSize) {
            message = 'Failed to retrieve resized image dimensions.';
        } else {
            // Split dimensions string and parse integers
            const originalDimensions = resizedImageSize.split('x');
            const originalWidth = parseInt(originalDimensions[0]);
            const originalHeight = parseInt(originalDimensions[1]);

            // Compare original dimensions with target dimensions
            if (originalWidth === targetWidth && originalHeight === targetHeight) {
                message = `Image has correct dimensions (${targetWidth}x${targetHeight} pixels).`;
            } else if (originalWidth < targetWidth || originalHeight < targetHeight) {
                message = `Image is smaller than desired dimensions (${originalWidth}x${originalHeight} pixels).`;
            } else {
                message = `Image was resized to ${targetWidth}x${targetHeight} pixels.`;
            }
        }

        // Prepare response with the message
        return new Response(message, {
            headers: {
                'Content-Type': 'text/plain'
            }
        });
    } catch (error) {
        // Handle and log any errors that occur
        console.error('Error fetching or processing image:', error);
        return new Response('Error fetching or processing image', {
            status: 500,
            headers: {
                'Content-Type': 'text/plain'
            }
        });
    }
}

fetchAndProcessImage(options)
    .then(response => {
        console.log(response);
    })
    .catch(error => {
        console.error('Error processing image:', error);
    });
