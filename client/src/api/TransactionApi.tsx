export class Transaction {
  group: string = "";
  payer: string = "";
  subtotal: number = 0;
  tax: number = 0;
  tip: number = 0;
  memo: string = "";
  participants: Participant[] = [];
}

export class Participant {
  name: string = "";
  amount: number = 0;
}

/**
 * Posts a transaction to the API.
 * @param transaction The transaction to post.
 * @returns The UUID of the transaction.
 */
async function postTransaction(transaction: Transaction): Promise<string> {
  var response = "";
  const url = process.env.REACT_APP_API_ENDPOINT + "/transaction";
  console.log("url: " + url);
  await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(transaction),
  })
    .then((response) => response.json())
    .then((response) => {
      console.log("Success:", response);
      response = response;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  return response;
}

export default postTransaction;
