import {
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
  IonInput,
  IonItem,
  IonLabel,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle,
  IonButton,
  IonCheckbox,
  useIonAlert,
} from "@ionic/react";
import "./Tab2.css";
import React, { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { Report } from "../api/ReportApi";
import getReport from "../api/ReportApi";
import { Preferences } from "@capacitor/preferences";

const Tab2: React.FC = () => {
  const [hasClicked, setHasClicked] = useState(false);
  const [showHideTotals, setShowHideTotals] = useState(false);
  const [showHideTransactions, setShowHideTransactions] = useState(false);

  const [groupName, setGroupName] = useState("");

  const [report, setReport] = useState(new Report());

  const [presentAlert] = useIonAlert();

  const handleToggle = () => {
    if (!hasClicked) {
      setShowHideTotals(!showHideTotals);
      setHasClicked(true);
    }
  };

  let initialValues = {
    group: "",
    reset: false,
  };

  async function isAuthenticated() {
    await Preferences.set({
      key: "userId",
      value: "123",
    });
    const { value } = await Preferences.get({ key: "userId" });
    console.log(value);
    return value !== null;
  }

  const { handleSubmit, control, reset, watch, getValues } = useForm({
    defaultValues: { ...initialValues },
    mode: "onChange",
  });
  const onSubmit = async (data: any) => {
    if (await isAuthenticated()) {
      await getReport(data.group.toLowerCase().trim(), data.reset)
        .then((response) => {
          handleToggle();
          setReport(response);
        })
        .catch((error) => {
          console.log("failed");
          presentAlert({
            header: "Error",
            message: error,
            buttons: ["OK"],
          });
        });
      reset(initialValues);
    } else {
      if (data.reset) {
        presentAlert({
          header: "Error",
          message: "You must login to reset values.",
          buttons: ["OK"],
        });
      } else {
        await getReport(data.group, false)
          .then((response) => {
            handleToggle();
            setReport(response);
          })
          .catch((error) => {
            console.log("failed");
            presentAlert({
              header: "Error",
              message: error,
              buttons: ["OK"],
            });
          });
      }
    }
    setGroupName(data.group);
  };
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Generate Report</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Generate Report</IonTitle>
          </IonToolbar>
        </IonHeader>
        <form className="ion-padding" onSubmit={handleSubmit(onSubmit)}>
          <IonItem>
            <IonLabel>Group</IonLabel>
            <Controller
              control={control}
              name="group"
              render={({ field: { value, onChange } }) => (
                <IonInput
                  value={value}
                  onIonChange={({ detail: { value } }) => onChange(value)}
                />
              )}
            />
          </IonItem>
          <IonItem lines="none">
            <IonLabel>Reset Tab</IonLabel>
            <Controller
              control={control}
              name="reset"
              render={({ field: { value, onChange } }) => (
                <IonCheckbox
                  slot="start"
                  checked={value}
                  onIonChange={({ detail: { checked } }) => onChange(checked)}
                />
              )}
            />
          </IonItem>
          <IonButton
            className="ion-margin-top"
            type="submit"
            expand="block"
            disabled={watch("group") == ""}
          >
            Submit
          </IonButton>
        </form>
        {/* show report in card */}
        {showHideTotals ? (
          <>
            <IonCard>
              <IonCardHeader>
                <IonCardTitle>{groupName} Totals</IonCardTitle>
              </IonCardHeader>
              <IonCardContent>
                {report.report.map((reportLine, i) => (
                  <div key={i}>
                    <li>{reportLine}</li>
                  </div>
                ))}
              </IonCardContent>
            </IonCard>
            <div className="ion-padding">
              <IonButton
                className="ion-margin-top"
                expand="block"
                onClick={() => setShowHideTransactions(!showHideTransactions)}
              >
                Toggle Individual Transactions
              </IonButton>
            </div>
            {showHideTransactions ? (
              <>
                {report.transactions.map((transaction, i) => (
                  <IonCard>
                    <IonCardHeader>
                      <IonCardTitle>{transaction.memo}</IonCardTitle>
                    </IonCardHeader>
                    <IonCardContent>
                      {transaction.participants.map((participant, i) => (
                        <div key={i}>
                          <li>
                            {participant.name} owes {transaction.purchaser}
                            {" $"}
                            {participant.amount.toFixed(2)}
                          </li>
                        </div>
                      ))}
                    </IonCardContent>
                  </IonCard>
                ))}
              </>
            ) : (
              <></>
            )}
          </>
        ) : (
          <></>
        )}
      </IonContent>
    </IonPage>
  );
};

export default Tab2;
