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
} from "@ionic/react";
import ExploreContainer from "../components/ExploreContainer";
import logo from "../logo.png";
import { useForm, Controller } from "react-hook-form";
import "./Tab1.css";
import { alertCircleOutline } from "ionicons/icons";

const Tab1: React.FC = () => {
  // let initialValues = {
  //   group: "",
  //   payer: "",
  //   subtotal: "",
  //   tax: "",
  //   tip: "",
  //   memo: "",
  //   Participants: [],
  //   reset: false,
  // };

  const {
    handleSubmit,
    control,
    reset,
    watch,
    getValues,
    register,
    formState: { errors },
  } = useForm({
    // defaultValues: { ...initialValues },
    mode: "onChange",
  });

  const fields = [
    {
      label: "Group",
      rules: {
        required: true,
        maxLength: 32,
      },
      props: {
        name: "group",
        type: "text",
        inputMode: "text",
      },
    },
    {
      label: "Payer",
      rules: {
        required: true,
        maxLength: 32,
      },
      props: {
        name: "payer",
        type: "text",
        inputMode: "text",
      },
    },
    {
      label: "Subtotal",
      rules: {
        required: true,
      },
      props: {
        name: "subtotal",
        type: "number",
        inputMode: "numeric",
      },
    },
    {
      label: "Tax",
      rules: {
        required: false,
      },
      props: {
        name: "tax",
        type: "number",
        inputMode: "numeric",
      },
    },
    {
      label: "Tip",
      rules: {
        required: false,
      },
      props: {
        name: "tip",
        type: "number",
        inputMode: "numeric",
      },
    },
    {
      label: "Memo",
      rules: {
        required: true,
        maxLength: 140,
      },
      props: {
        name: "memo",
        type: "text",
        inputMode: "text",
      },
    },
  ];

  const onSubmit = async (data: any) => {
    console.log(getValues());
  };

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
        <form onSubmit={handleSubmit(onSubmit)}>
          {fields.map((field, index) => {
            const { label, rules, props } = field;

            return (
              <IonItem key={`form_field_${index}`} lines="full">
                <>
                  <IonLabel position="floating">{label}</IonLabel>
                  <Controller
                    control={control}
                    name={props.name}
                    rules={rules}
                    render={({
                      fieldState: { invalid, error },
                      field: { value, onChange },
                    }) => (
                      <IonInput
                        type={props.type as any}
                        value={value}
                        onIonChange={({ detail: { value } }) => onChange(value)}
                      />
                    )}
                  />
                </>
              </IonItem>
            );
          })}
          <IonButton className="ion-margin-top" type="submit" expand="block">
            Submit
          </IonButton>
        </form>
      </IonContent>
    </IonPage>
  );
};

export default Tab1;
