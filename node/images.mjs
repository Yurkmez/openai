import fs from "fs";
import path from "path";
import { Readable } from "stream";
import { finished } from "stream/promises";
import openai from "./utils/openai.mjs";
import { generateFileNameWithExtension } from "./utils/fileUtils.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";

const __dirname = import.meta.dirname;

const prompt =
  "sun is shining in the early morning while two fisherman are sitting near the river";

try {
  const response = await openai.images.generate({
    model: "dall-e-3",
    prompt,
    n: 1,
    size: "1024x1024",
  });

  // console.log(response);

  const imageUrl = response.data[0].url;
  // console.log(imageUrl);

  const imagesDir = path.join(__dirname, "images");
  if (!fs.existsSync(imagesDir)) {
    fs.mkdirSync(imagesDir, { recursive: true });
  }

  const fileName = generateFileNameWithExtension({
    prompt,
    url: imageUrl,
    imagesDir,
  });
  const filePath = path.join(imagesDir, fileName);

  try {
    // Attempt to download the image
    const imageResponse = await fetch(imageUrl);
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
