import React, { useState } from "react";
import { loginUser } from "../api/authService";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../components/AuthProvider";
import AuthLayout from "../components/AuthLayout";
import FormInput from "../components/FormInput";
import FormButton from "../components/FormButton";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();
  const location = useLocation(); // To get the success message
  const { login } = useAuth();

  // Check if we were redirected from registration
  const successMessage = location.state?.message;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const response = await loginUser(email, password);
      login(response.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      // --- NEW ROBUST ERROR HANDLING ---
      let errorMsg = "Login failed. Please check your credentials."; // Default

      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;

        if (typeof detail === "string") {
          // This is a simple string error (like our 401 "Incorrect email")
          errorMsg = detail;
        } else if (Array.isArray(detail) && detail[0]?.msg) {
          // This is a Pydantic/FastAPI 422 validation error
          errorMsg = `${detail[0].loc[1]}: ${detail[0].msg}`;
        }
      }
      setError(errorMsg);
      // --- END NEW HANDLING ---
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Sign in to your account"
      footerText="Don't have an account?"
      footerLink="/register"
    >
      {/* Show success message from registration */}
      {successMessage && !error && (
        <div className="mb-4 p-3 rounded-md bg-mint-green text-green-900 text-sm">
          {successMessage}
        </div>
      )}

      {/* Show login error */}
      {error && (
        <div className="mb-4 p-3 rounded-md bg-error-red text-red-900 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <FormInput
          id="email"
          label="Email address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />

        <FormInput
          id="password"
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="current-password"
        />

        <div>
          <FormButton isLoading={isLoading}>Sign In</FormButton>
        </div>
      </form>
    </AuthLayout>
  );
}

export default Login;
