import { URL } from "url";
import fs from "fs";
import path from "path";
import { DateTime } from "luxon";

export function generateFileNameWithExtension({ prompt, url, imagesDir }) {
  // Convert the prompt to lowercase, replace spaces with underscores, and limit to 25 characters
  const baseFileName = prompt
    .toLowerCase()
    .split(" ")
    .slice(0, 25)
    .join("_")
    .substring(0, 25);

  const extension = (url && getImageExtension(url)) || "png";

  const version = getNextVersionNumber(baseFileName, extension, imagesDir);
  return `${baseFileName}_v${version}.${extension}`;
}

export function getNextVersionNumber(baseFileName, extension, imagesDir) {
  const filePattern = new RegExp(`^${baseFileName}_v(\\d+)\\.${extension}$`);
  let highestVersion = 0;

  const existingFiles = fs.readdirSync(imagesDir);

  existingFiles.forEach((file) => {
    const match = file.match(filePattern);
    if (match) {
      const fileVersion = parseInt(match[1], 10);
      if (fileVersion > highestVersion) {
        highestVersion = fileVersion;
      }
    }
  });

  return highestVersion + 1;
}

export function getImageExtension(url) {
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

export function saveImageDataToJson({
  imageMetaData,
  imagesDir,
  base64ImageData,
}) {
  try {
    const jsonFilePath = path.join(imagesDir, "images.json");

    // Load existing data if the file exists
    let images = [];
    if (fs.existsSync(jsonFilePath)) {
      const jsonData = fs.readFileSync(jsonFilePath, "utf8");
      images = JSON.parse(jsonData);
    }

    // Append the new image data
    images.push({
      ...imageMetaData,
      date: DateTime.now().toFormat("d-M-yyyy"),
      base64: base64ImageData,
    });

    // Save all data back to the JSON file
    fs.writeFileSync(jsonFilePath, JSON.stringify(images, null, 2), "utf8");
    console.log("Image data saved successfully to JSON file:", jsonFilePath);
  } catch (error) {
    console.error("Error saving image data to JSON:", error.message);
  }
}
