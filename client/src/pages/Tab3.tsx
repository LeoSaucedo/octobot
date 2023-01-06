import {
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
  IonInput,
  IonItem,
  IonLabel,
  IonList,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonButton,
  IonCheckbox,
  IonRow,
  IonCol,
  IonGrid,
} from "@ionic/react";
import ExploreContainer from "../components/ExploreContainer";
import "./Tab3.css";

import { useForm, useWatch, Control } from "react-hook-form";

type FormValues = {
  groupName: string;
};

function IsolateReRender({ control }: { control: Control<FormValues> }) {
  const group = useWatch({
    control,
    name: "groupName",
    defaultValue: "",
  });

  return <div>{group}</div>;
}

const Tab3: React.FC = () => {
  const { register, control, handleSubmit } = useForm<FormValues>();
  const onSubmit = handleSubmit((data) => console.log(data));
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Tab 3</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Tab 3</IonTitle>
          </IonToolbar>
        </IonHeader>
        <form onSubmit={onSubmit}>
          <IonGrid>
            <IonRow class="ion-justify-content-center">
              <IonItem>
                <IonLabel position="floating">Group Name</IonLabel>
                <IonInput {...register("groupName")} />
              </IonItem>
            </IonRow>
            <br />
            <IonRow class="ion-justify-content-center">
              <IonButton type="submit" expand="block">
                Submit
              </IonButton>
            </IonRow>
          </IonGrid>
          <IsolateReRender control={control} />
        </form>
      </IonContent>
    </IonPage>
  );
};

export default Tab3;
