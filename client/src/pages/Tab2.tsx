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
} from "@ionic/react";
import "./Tab2.css";
import React, { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { Report } from "../api/ReportApi";
import getReport from "../api/ReportApi";

const Tab2: React.FC = () => {
  const [hasClicked, setHasClicked] = useState(false);
  const [showHide, setShowHide] = useState(false);

  const [report, setReport] = useState(new Report());

  const handleToggle = () => {
    if (!hasClicked) {
      setShowHide(!showHide);
      setHasClicked(true);
    }
  };

  let initialValues = {
    group: "",
    reset: false,
  };

  const { handleSubmit, control, reset, watch } = useForm({
    defaultValues: { ...initialValues },
    mode: "onChange",
  });
  const onSubmit = async (data: any) => {
    console.log("URL: " + process.env.REACT_APP_API_ENDPOINT);
    console.log(data);
    handleToggle();
    await getReport(data.group, data.reset).then((response) => {
      console.log("This is a test:", response);
      setReport(response);
    });
    reset(initialValues);
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
            <IonLabel position="floating">Group</IonLabel>
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
        {showHide ? (
          <IonCard>
            <IonCardHeader>
              <IonCardTitle>Card Title</IonCardTitle>
            </IonCardHeader>
            <IonCardContent>{report.report}</IonCardContent>
          </IonCard>
        ) : (
          <span></span>
        )}
      </IonContent>
    </IonPage>
  );
};

export default Tab2;