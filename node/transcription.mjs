import fs from "fs";
import path from "path";
import openai from "./utils/openai.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";

const __dirname = import.meta.dirname;

const model = "whisper-1";
const fileName = "test_v1.m4a";

const dir = path.join(__dirname, "audio", "m4a");
const filePath = path.join(dir, fileName);

try {
  const response = await openai.audio.transcriptions.create({
    model,
    file: fs.createReadStream(filePath),
    response_format: "json", // default
  });

  console.log(response);

  fs.appendFileSync(
    path.join(dir, "transcriptions.txt"),
    `${response.text}\n\n`
  );
} catch (error) {
  openaiErrorHandler(error);
}
