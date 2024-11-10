import { URL } from "url";
import fs from "fs";

export function generateFileNameWithExtension(prompt, url, imagesDir) {
  // Convert the prompt to lowercase, replace spaces with underscores, and limit to 25 characters
  const baseFileName = prompt
    .toLowerCase()
    .split(" ")
    .slice(0, 25)
    .join("_")
    .substring(0, 25);

  const extension = getImageExtension(url) || "png";

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
