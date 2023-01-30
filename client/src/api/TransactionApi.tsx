export class Transaction {
  id: string = "";
  group: string = "";
  payer: string = "";
  subtotal: number = 0;
  tax: number = 0;
  tip: number = 0;
  memo: string = "";
  participants: Participant[] = [];
  ip: string = "";
}

export class Participant {
  name: string = "";
  amount: number = 0;
}

export class ResponseObj {
  amount: number = 0;
  debtor: string = "";
  group_name: string = "";
  id: string = "";
  is_paid: number = 0;
  memo: string = "";
  purchaser: string = "";
  transaction_id: string = "";
}

/**
 * Posts a transaction to the API.
 * @param transaction The transaction to post.
 * @returns The response object.
 */
async function postTransaction(
  transaction: Transaction
): Promise<ResponseObj[]> {
  console.log(transaction);
  var response = [new ResponseObj()];
  const url = process.env.REACT_APP_API_ENDPOINT + "/transaction";
  console.log("url: " + url);
  await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(transaction),
  })
    .then((res) => res.json())
    .then((res) => {
      console.log("Success:", res);
      response = res;
    })
    .catch((error) => {
      console.error("Error:", error);
      throw error;
    });
  return response;
}

export default postTransaction;
