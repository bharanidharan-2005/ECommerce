import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import App from "./App.jsx";
import { SettingsProvider } from "./context/SettingsContext.jsx";
import { store } from "./app/store";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <SettingsProvider>
          <App />
        </SettingsProvider>
        {/* Bottom-right, non-intrusive confirmation popups (e.g. "added to cart") */}
        <ToastContainer
          position="bottom-right"
          autoClose={2200}
          newestOnTop
          limit={3}
          pauseOnFocusLoss={false}
          theme="light"
        />
      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);
