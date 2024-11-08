import OpenAI from "openai";
import "dotenv/config";

const openai = new OpenAI();

// console.log(process.env.OPENAI_API_KEY);

const completion = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  max_tokens: 300,
  n: 2,
  messages: [
    {
      role: "system",
      content:
        "Ты настроен на веселый разговор. Выводи только одну короткую историю не больше 20 слов",
    },
    {
      role: "user",
      content: "Напиши историю о программистах",
    },
  ],
});

console.log(completion);

completion.choices.forEach((choice) => {
  console.log(choice.message);
});
