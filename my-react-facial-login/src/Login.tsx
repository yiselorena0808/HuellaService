import React, { useRef, useState } from "react";
import Webcam from "react-webcam";

const videoConstraints = {
  width: 300,
  height: 300,
  facingMode: "user",
};

const SERVER = "http://localhost:8000";

export const Login = () => {
  const webcamRef = useRef<Webcam>(null);
  const [message, setMessage] = useState("");
  const [username, setUsername] = useState("");

  const capture = async (endpoint: string) => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (!imageSrc) return;

    const form = new FormData();
    form.append("image", imageSrc);
    if (endpoint === "/register-face") form.append("username", username);

    try {
      const res = await fetch(`${SERVER}${endpoint}`, {
        method: "POST",
        body: form,
      });

      const data = await res.json();
      if (res.ok) {
        setMessage(endpoint === "/register-face"
          ? ` Usuario registrado: ${data.msg}`
          : ` Bienvenido ${data.username}`);
      } else {
        setMessage(`Error: ${data.detail}`);
      }
    } catch (err) {
      setMessage("Error en el servidor.");
    }
  };

  return (
    <div>
      <Webcam
        audio={false}
        height={300}
        screenshotFormat="image/jpeg"
        width={300}
        ref={webcamRef}
        videoConstraints={videoConstraints}
      />
      <input
        type="text"
        placeholder="Nombre de usuario"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <div>
        <button onClick={() => capture("/register-face")}>Registrar rostro</button>
        <button onClick={() => capture("/verify-face")}>Iniciar sesión</button>
      </div>
      <p>{message}</p>
    </div>
  );
};

