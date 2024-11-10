import { URL } from "url";

export function generateFileNameWithExtension(prompt, url) {
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
