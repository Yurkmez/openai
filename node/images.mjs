import { OpenAIError } from "openai";
// import openai from "./utils/openai.mjs";
import { URL } from "url";

function generateFileName(prompt, url) {
  // Convert the prompt to lowercase, replace spaces with underscores, and limit to 25 characters
  const baseFileName = prompt
    .toLowerCase()
    .split(" ")
    .slice(0, 25)
    .join("_")
    .substring(0, 25);

  const extension = getImageExtension(url);

  return extension ? `${baseFileName}.${extension}` : baseFileName;
}

function getImageExtension(url) {
  try {
    const parsedUrl = new URL(url);
    const pathname = parsedUrl.pathname;
    const extension = pathname.split(".").pop(); // Get the last part after the dot
    return extension;
  } catch (error) {
    console.error("Invalid URL:", error);
    return null;
  }
}

const prompt = "blogger setup with notebook and camera";

// const response = await openai.images.generate({
//   model: "dall-e-3",
//   prompt,
//   n: 1,
//   size: "1024x1024",
// });

// console.log(response);

// const image_url = response.data[0].url;
// console.log(image_url);

const image_url = "YOUR IMAGE URL";

const fileName = generateFileName(prompt, image_url);
console.log(fileName);
