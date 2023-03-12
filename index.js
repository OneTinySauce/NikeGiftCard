async function getBalance(num, pin) {
    const url = "https://cors-anywhere.herokuapp.com/https://api.nike.com/payment/giftcard_balance/v1/";
  
    const headers = {
        'authority': 'api.nike.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'appid': 'orders',
        'origin': 'https://www.nike.com',
        'referer': 'https://www.nike.com/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-nike-visitid': '2',
        'x-nike-visitorid': '2c2b7ed6-99db-451e-2213-ecf4bb180c6e',
    };

    const data = {
        'accountNumber': num,
        'currency': 'USD',
        'pin': pin,
    };
  
    try {
        const response = await fetch(url, {
          method: "POST",
          headers: headers,
          body: JSON.stringify(data)
        });
        const balance = await response.json();
        console.log(balance);
        document.getElementById("show").innerHTML = balance
      } catch (error) {
        console.error(error);
      }
  }
  
//   console.log(getBalance("6060106931447066893", "049155"));
  