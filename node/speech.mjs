import fs from "fs";
import path from "path";
import openai from "./utils/openai.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";
import { generateFileNameWithExtension } from "./utils/fileUtils.mjs";

const __dirname = import.meta.dirname;

const input =
  "Креативность и инновации движут будущее, вдохновляя на прогресс и открытия. Каждая идея начинается с искры";
const model = "tts-1";
const voice = "shimmer";
const extension = "mp3";

try {
  const response = await openai.audio.speech.create({
    model,
    input,
    voice,
    response_format: extension,
  });

  // console.log(response);

  const audioData = await response.arrayBuffer();

  if (audioData) {
    const dir = path.join(__dirname, "audio", extension);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    const fileName = generateFileNameWithExtension({
      dir,
      prompt: input,
      extension,
    });
    const filePath = path.join(dir, fileName);

    // Save audio file
    const audioBuffer = Buffer.from(audioData);
    fs.writeFileSync(filePath, audioBuffer);
    console.log("Successfully saved audio:", fileName);
  } else {
    console.error("Error: Audio data wasn't received");
  }
} catch (error) {
  openaiErrorHandler(error);
}
