import OpenAI, { OpenAIError } from "openai";
import "dotenv/config";

if (!process.env.OPENAI_API_KEY) {
  console.error(
    "Error: The OPENAI_API_KEY environment variable is missing or empty.\nPlease add it to the .env file."
  );
  process.exit(1);
}

const openai = new OpenAI();

// console.log(process.env.OPENAI_API_KEY);
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
  if (error instanceof OpenAIError) {
    console.error("OpenAI Error:", error.message);
  } else {
    console.error("Some error occured:", error.message);
  }
}
