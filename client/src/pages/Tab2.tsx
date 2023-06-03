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
  IonCardSubtitle,
  IonIcon,
  IonModal,
  IonButtons,
} from "@ionic/react";
import "./Tab2.css";
import React, { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { Report, Transaction } from "../api/ReportApi";
import { helpCircleOutline } from "ionicons/icons";
import getReport from "../api/ReportApi";
import transactionApi from "../api/TransactionApi";
import { Preferences } from "@capacitor/preferences";

const Tab2: React.FC = () => {
  const [hasClicked, setHasClicked] = useState(false);
  const [showHideTotals, setShowHideTotals] = useState(false);
  const [showHideTransactions, setShowHideTransactions] = useState(false);
  const [showHideSimplifyModal, setShowHideSimplifyModal] = useState(false);

  const [groupName, setGroupName] = useState("");
  const [simplify, setSimplify] = useState(false);

  const [report, setReport] = useState(new Report());

  const [presentAlert] = useIonAlert();

  /**
   * shows report totals card on generate report form submission
   */
  const handleShowReport = () => {
    if (!hasClicked) {
      setShowHideTotals(!showHideTotals);
      setHasClicked(true);
    }
  };

  let initialValues = {
    group: "",
    reset: false,
    simplify: false,
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

  async function fetchReport(
    groupName: string,
    reset: boolean,
    simplify: boolean
  ) {
    await getReport(groupName.toLowerCase().trim(), reset, simplify)
      .then((response) => {
        handleShowReport();
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

  const { handleSubmit, control, reset, watch, getValues } = useForm({
    defaultValues: { ...initialValues },
    mode: "onChange",
  });
  const onSubmit = async (data: any) => {
    setShowHideTransactions(false);
    if (await isAuthenticated()) {
      await fetchReport(data.group, data.reset, data.simplify);
      reset(initialValues);
    } else {
      if (data.reset) {
        presentAlert({
          header: "Error",
          message: "You must login to reset values.",
          buttons: ["OK"],
        });
      } else {
        await fetchReport(data.group, false, data.simplify);
      }
    }
    setGroupName(data.group);
    setSimplify(data.simplify);
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
          <IonItem lines="none">
            <IonLabel>Simplify Payments</IonLabel>
            <Controller
              control={control}
              name="simplify"
              render={({ field: { value, onChange } }) => (
                <IonCheckbox
                  slot="start"
                  checked={value}
                  onIonChange={({ detail: { checked } }) => onChange(checked)}
                />
              )}
            />
            <IonButton
              type="button"
              fill="clear"
              color="medium"
              onClick={() => setShowHideSimplifyModal(true)}
            >
              <IonIcon slot="icon-only" icon={helpCircleOutline}></IonIcon>
            </IonButton>
            <IonModal isOpen={showHideSimplifyModal}>
              <IonHeader>
                <IonToolbar>
                  <IonTitle>Payment Simplification</IonTitle>
                  <IonButtons slot="end">
                    <IonButton onClick={() => setShowHideSimplifyModal(false)}>
                      Close
                    </IonButton>
                  </IonButtons>
                </IonToolbar>
              </IonHeader>
              <IonContent className="ion-padding">
                <p>
                  <strong>Payment simplification</strong> (a.k.a. "
                  <em>simplify payments</em>" or "<em>payment rearrangement</em>
                  ") is a feature of <strong>Octobot</strong> that restructures
                  payments within a group and among friends. It doesn't alter
                  the overall amount owed by anyone, but it streamlines the
                  process of reimbursing individuals by reducing the total
                  number of payments.
                </p>

                <p>
                  For instance, let's consider a scenario where{" "}
                  <strong>Alex, Bryan, and Carlos</strong> share an apartment.
                  Alex owes Bryan $20, and Bryan owes Carlos $20. Instead of
                  initiating two separate payments, <strong>Octobot</strong>{" "}
                  would advise Alex to directly pay $20 to Carlos, thus
                  minimizing the total number of transactions. This ensures
                  faster and more efficient repayment for everyone involved.
                </p>
              </IonContent>
            </IonModal>
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
                  <div key={i}>
                    <IonCard>
                      <IonCardHeader>
                        <IonCardTitle>{transaction.memo}</IonCardTitle>
                        <IonCardSubtitle>
                          {transaction.timestamp}
                        </IonCardSubtitle>
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
                      <IonButton
                        fill="clear"
                        color="danger"
                        onClick={async () => {
                          presentAlert({
                            header: "Delete Transaction",
                            message:
                              "Are you sure you want to delete this transaction?",
                            buttons: [
                              {
                                text: "Cancel",
                                role: "cancel",
                              },
                              {
                                text: "OK",
                                role: "confirm",
                                handler: async () => {
                                  await transactionApi
                                    .deleteTransaction(transaction.id)
                                    .then(async () => {
                                      await fetchReport(
                                        groupName,
                                        false,
                                        simplify
                                      );
                                    });
                                },
                              },
                            ],
                          });
                        }}
                      >
                        Delete Transaction
                      </IonButton>
                    </IonCard>
                  </div>
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
