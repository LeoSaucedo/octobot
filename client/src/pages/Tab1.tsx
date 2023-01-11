import {
  IonContent,
  IonHeader,
  IonImg,
  IonPage,
  IonTitle,
  IonToolbar,
  IonItem,
  IonLabel,
  IonInput,
  IonCheckbox,
  IonButton,
  IonButtons,
  IonAvatar,
  IonIcon,
  IonText,
  IonNote,
  useIonAlert,
  IonCard,
  IonCardHeader,
  IonCardContent,
  IonCardTitle,
  IonCardSubtitle,
} from "@ionic/react";
import ExploreContainer from "../components/ExploreContainer";
import logo from "../logo.png";
import { useForm, Controller, useFieldArray } from "react-hook-form";
import "./Tab1.css";
import { alertCircleOutline, closeCircleOutline } from "ionicons/icons";
import React, { useState } from "react";
import postTransaction, { Transaction } from "../api/TransactionApi";
import { ResponseObj } from "../api/TransactionApi";
import { report } from "process";
import { Preferences } from "@capacitor/preferences";

type FormValues = {
  group: string;
  payer: string;
  subtotal: string;
  tax: string;
  tip: string;
  memo: string;
  participants: {
    name: string;
    amount: string;
  }[];
};

const Tab1: React.FC = () => {
  const [hasClicked, setHasClicked] = useState(false);
  const [showHide, setShowHide] = useState(false);
  const handleToggle = () => {
    if (!hasClicked) {
      setShowHide(!showHide);
      setHasClicked(true);
    }
  };

  const [presentAlert] = useIonAlert();

  const [ip, setIp] = useState<string>("");

  const [responses, setResponses] = useState<ResponseObj[]>([]);
  let initialValues = {
    group: "",
    payer: "",
    subtotal: "",
    tax: "",
    tip: "",
    memo: "",
    participants: [
      {
        name: "",
        amount: "",
      },
    ],
  };

  const {
    register,
    reset,
    formState: { errors },
    handleSubmit,
    control,
  } = useForm({
    defaultValues: { ...initialValues },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "participants",
    rules: {
      required: `You must have at least one participant.`,
      // validate: () => {
      //   return true;
      // },
    },
  });

  async function isAuthenticated() {
    //TODO: npx cap sync
    await Preferences.set({
      key: "userId",
      value: "123",
    });
    const { value } = await Preferences.get({ key: "userId" });
    return value != null;
  }

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Add Transaction</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Add Transaction</IonTitle>
          </IonToolbar>
        </IonHeader>
        <form
          className="ion-padding"
          onSubmit={handleSubmit(async (data) => {
            console.log(data);
            if (ip == "") {
              await fetch("https://ipapi.co/json/")
                .then((response) => response.json())
                .then((data) => setIp(data.ip));
            }
            var transaction: Transaction = {
              group: data.group.toLowerCase(),
              payer: data.payer.toLowerCase(),
              subtotal: parseFloat(data.subtotal),
              tax: parseFloat(data.tax),
              tip: parseFloat(data.tip),
              memo: data.memo,
              ip: ip,
              participants: data.participants.map((participant) => {
                return {
                  name: participant.name.toLowerCase(),
                  amount: parseFloat(participant.amount),
                };
              }),
            };
            if (await isAuthenticated()) {
              postTransaction(transaction)
                .then((response) => {
                  setResponses(response);
                  console.log(response);
                  handleToggle();
                })
                .then(() => {
                  reset(initialValues);
                })
                .catch((error) => {
                  presentAlert({
                    header: "Error",
                    message: error,
                    buttons: ["OK"],
                  });
                });
            } else {
              presentAlert({
                header: "Error",
                message: "You must be logged in to submit a transaction.",
                buttons: ["OK"],
              });
            }
          })}
        >
          <IonItem>
            <IonLabel>Group</IonLabel>
            <IonInput
              required={true}
              {...register(`group`, { required: true })}
            ></IonInput>
          </IonItem>
          <IonItem>
            <IonLabel>Payer</IonLabel>
            <IonInput
              required={true}
              {...register(`payer`, { required: true })}
            ></IonInput>
          </IonItem>
          <IonItem>
            <IonLabel>Subtotal $</IonLabel>
            <IonInput
              type="number"
              step="0.01"
              placeholder="0.00"
              required={true}
              {...register(`subtotal`, {
                required: true,
                valueAsNumber: true,
              })}
            ></IonInput>
          </IonItem>
          <IonItem>
            <IonLabel>Tax $</IonLabel>
            <IonInput
              type="number"
              step="0.01"
              placeholder="0.00"
              {...register(`tax`, { valueAsNumber: true })}
            ></IonInput>
          </IonItem>
          <IonItem>
            <IonLabel>Tip $</IonLabel>
            <IonInput
              type="number"
              step="0.01"
              placeholder="0.00"
              {...register(`tip`, { valueAsNumber: true })}
            ></IonInput>
          </IonItem>
          <IonItem>
            <IonLabel>Memo</IonLabel>
            <IonInput
              required={true}
              {...register(`memo`, { required: true })}
            ></IonInput>
          </IonItem>
          <IonItem lines="none">
            <IonLabel>
              <b>Participants</b>
            </IonLabel>
          </IonItem>
          {fields.map((field, index) => {
            return (
              <section key={index}>
                <IonItem>
                  <IonInput
                    placeholder="Name"
                    required={true}
                    {...register(`participants.${index}.name`, {
                      required: true,
                    })}
                  />
                  <IonLabel>$</IonLabel>
                  <IonInput
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    {...register(`participants.${index}.amount`, {
                      valueAsNumber: true,
                    })}
                  ></IonInput>
                  <IonButton
                    type="button"
                    color="danger"
                    fill="clear"
                    onClick={() => remove(index)}
                  >
                    <IonIcon
                      slot="icon-only"
                      icon={closeCircleOutline}
                    ></IonIcon>
                  </IonButton>
                </IonItem>
              </section>
            );
          })}
          <IonItem lines="none">
            <IonButton
              fill="outline"
              color="success"
              type="button"
              onClick={() => {
                append({
                  name: "",
                  amount: "",
                });
              }}
            >
              Add Participant
            </IonButton>
          </IonItem>
          <IonText color="danger">{errors.participants?.root?.message}</IonText>
          <IonButton className="ion-margin-top" type="submit" expand="block">
            {" "}
            Submit
          </IonButton>
        </form>
        {showHide ? (
          <IonCard>
            <IonCardHeader>
              <IonCardTitle>Transaction Summary</IonCardTitle>
              <IonCardSubtitle>{responses[0].memo}</IonCardSubtitle>
            </IonCardHeader>
            <IonCardContent>
              {responses.map((response, i) => (
                <div key={i}>
                  <li>
                    {response.debtor} owes {response.purchaser} $
                    {response.amount.toFixed(2)}.
                  </li>
                </div>
              ))}
            </IonCardContent>
          </IonCard>
        ) : (
          <span></span>
        )}
      </IonContent>
    </IonPage>
  );
};

export default Tab1;
