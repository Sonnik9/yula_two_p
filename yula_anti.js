const axios = require("axios");
const Captcha = require("2captcha");

const solver = new Captcha.Solver("c58a05fef7d7bbf00ac85120f3da6f27");

const registration = async () => {
  console.log("Solving captcha...");
  //This api key is invalid
  const { data } = await solver.hcaptcha(
    "6Lf39AMTAAAAALPbLZdcrWDa8Ygmgk_fmGmrlRog",
    "https://www.youtube.com/@PlaceholdersYT/about"
  );

  try {
    let res = await axios.post("https://www.youtube.com/@PlaceholdersYT/about", {
      fingerprint: "860858352775069716.iKrLWlYLj_GoTtd8MPCWria5RHI",
      email: "ytplaceholders@gmail.com",
      username: "example",
      password: "example",
      invite: null,
      consent: true,
      date_of_birth: "1995-06-04",
      gift_code_sku_id: null,
      captcha_key: data,
    });
    console.log(res.data);
  } catch (e) {
    console.log(e);
  }
};

registration();

// node yula_anti.js

{/* <a id="email" target="_blank" class="style-scope ytd-channel-about-metadata-renderer" href="mailto:ytplaceholders@gmail.com">ytplaceholders@gmail.com</a> */}