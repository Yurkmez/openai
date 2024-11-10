import fs from "fs";
import path from "path";
import { Readable } from "stream";
import { finished } from "stream/promises";
import openai from "./utils/openai.mjs";
import { generateFileNameWithExtension } from "./utils/fileUtils.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";

const __dirname = import.meta.dirname;

const prompt = "blogger setup with notebook and camera";

try {
  const response = await openai.images.generate({
    model: "dall-e-3",
    prompt,
    n: 1,
    size: "1024x1024",
  });

  // console.log(response);

  const image_url = response.data[0].url;
  // console.log(image_url);

  const imagesDir = path.join(__dirname, "images");
  if (!fs.existsSync(imagesDir)) {
    fs.mkdirSync(imagesDir, { recursive: true });
  }

  const fileName = generateFileNameWithExtension(prompt, image_url);
  const filePath = path.join(imagesDir, fileName);

  try {
    // Attempt to download the image
    const imageResponse = await fetch(image_url);
    if (!imageResponse.ok)
      throw new Error(`Failed to download image: ${imageResponse.statusText}`);

    // Check if the response is an image
    const contentType = imageResponse.headers.get("content-type");
    if (!contentType || !contentType.startsWith("image/")) {
      throw new Error(
        `The URL does not point to an image. Content-Type: ${contentType}`
      );
    }

    // Create a write stream and pipe the response to it
    const writeStream = fs.createWriteStream(filePath);
    await finished(Readable.fromWeb(imageResponse.body).pipe(writeStream));
    console.log("Successfully saved image:", fileName);
  } catch (error) {
    console.error("Error downloading image:", error);
  }
} catch (error) {
  openaiErrorHandler(error);
}
