import openai from "./utils/openai.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";

const systemContent = "Старайся отвечать кратко. Не более 15 слов";
const userContent = "Напиши историю о себе";

try {
  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    max_tokens: 300,
    n: 2,
    messages: [
      {
        role: "system",
        content: systemContent,
      },
      {
        role: "user",
        content: userContent,
      },
    ],
  });

  // console.log(completion);

  completion.choices.forEach((choice) => {
    console.log(choice.message);
  });
} catch (error) {
  openaiErrorHandler(error);
}
