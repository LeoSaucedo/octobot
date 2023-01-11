export class Report {
  report: string[] = [];
}

/**
 * Gets a report from the API.
 * @param groupName The group name to generate the report for.
 * @param reset Whether to reset the tab.
 * @returns The report data in the format: {"report":["Jerm owes bryan $41.91","Carlos owes bryan $42.55"]}
 */
async function getReport(groupName: string, reset: boolean): Promise<Report> {
  var report = new Report();
  const url =
    process.env.REACT_APP_API_ENDPOINT +
    "/report/" +
    groupName +
    "?reset=" +
    reset;
  console.log("url: " + url);
  await fetch(url, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((response) => {
      console.log("Success:", response);
      report = response;
    })
    .catch((error) => {
      console.error("Error:", error);
      throw error;
    });
  return report;
}

export default getReport;
