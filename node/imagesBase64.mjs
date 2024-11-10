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
    response_format: "b64_json",
    prompt,
    n: 1,
    size: "1024x1024",
  });

  // console.log(response);

  const base64ImageData = response.data[0].b64_json;
  // console.log(base64ImageData);

  if (base64ImageData) {
    const imagesDir = path.join(__dirname, "images");
    if (!fs.existsSync(imagesDir)) {
      fs.mkdirSync(imagesDir, { recursive: true });
    }

    const fileName = generateFileNameWithExtension({ imagesDir, prompt });
    const filePath = path.join(imagesDir, fileName);

    // Decode base64 and save image
    const imageBuffer = Buffer.from(base64ImageData, "base64");
    fs.writeFileSync(filePath, imageBuffer);
    console.log("Successfully saved image:", fileName);
  } else {
    console.error("Error: Image in base64 format wasn't received");
  }
} catch (error) {
  openaiErrorHandler(error);
}
