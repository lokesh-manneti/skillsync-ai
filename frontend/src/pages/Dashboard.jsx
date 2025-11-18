import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../components/AuthProvider";
import {
  uploadResume,
  getSkillGapAnalysis,
  getOptimizedResume,
  getResumeHistory,
} from "../api/authService";
import SkillGapReport from "../components/SkillGapReport";
import OptimizedResume from "../components/OptimizedResume";
import FormButton from "../components/FormButton";

function Dashboard() {
  const navigate = useNavigate();
  const { logout, isAuthenticated } = useAuth(); // <-- Get isAuthenticated

  // --- STATE ---
  const [resumeHistory, setResumeHistory] = useState([]);
  const [resumeSourceTab, setResumeSourceTab] = useState("upload"); // 'upload' or 'existing'
  const [selectedResumeId, setSelectedResumeId] = useState("");

  // Form State
  const [file, setFile] = useState(null);
  const [roleName, setRoleName] = useState("React Developer");
  const [learningPref, setLearningPref] = useState("Coding Projects");

  // App State
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("skillGap");

  // Results State
  const [skillGapResult, setSkillGapResult] = useState(null);
  const [optimizedResumeResult, setOptimizedResumeResult] = useState(null);

  // --- Fetch Resume History on Load (if authenticated) ---
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await getResumeHistory();
        setResumeHistory(response.data);
        // If user has history, default to selecting the latest one
        if (response.data.length > 0) {
          setSelectedResumeId(response.data[0].id); // Select the most recent
          setResumeSourceTab("existing"); // Default to the 'existing' tab
        }
      } catch (err) {
        console.error("Failed to fetch resume history:", err);
        // Don't set a user-facing error for this, just log it
      }
    };

    // Only run the fetch if we are authenticated
    if (isAuthenticated) {
      fetchHistory();
    }
  }, [isAuthenticated]); // <-- Dependency on isAuthenticated fixes the race condition

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // --- Main Analysis Submission Handler ---
  const handleSubmitAnalysis = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSkillGapResult(null);
    setOptimizedResumeResult(null);
    setActiveTab("skillGap");

    let resumeId = null;

    try {
      // Step 1: Get the resumeId (either from upload or selection)
      if (resumeSourceTab === "upload") {
        if (!file) {
          setError("Please upload a resume file.");
          setIsLoading(false);
          return;
        }
        const uploadResponse = await uploadResume(file);
        resumeId = uploadResponse.data.resume_id;

        // Refresh history after new upload and select the new resume
        const historyResponse = await getResumeHistory();
        setResumeHistory(historyResponse.data);
        setSelectedResumeId(resumeId); // Select the new one
      } else {
        if (!selectedResumeId) {
          setError("Please select an existing resume.");
          setIsLoading(false);
          return;
        }
        resumeId = selectedResumeId;
      }

      // Step 2 & 3: Run analyses in parallel
      const gapPromise = getSkillGapAnalysis(resumeId, roleName, learningPref);
      const optimizePromise = getOptimizedResume(resumeId, roleName);

      const [gapResponse, optimizeResponse] = await Promise.all([
        gapPromise,
        optimizePromise,
      ]);

      setSkillGapResult(gapResponse.data);
      setOptimizedResumeResult(optimizeResponse.data);
    } catch (err) {
      // Robust error handling
      console.error(err);
      let errorMsg = "An error occurred during analysis.";
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        if (typeof detail === "string") {
          errorMsg = detail;
        } else if (Array.isArray(detail) && detail[0]?.msg) {
          errorMsg = `${detail[0].loc[1]}: ${detail[0].msg}`;
        }
      }
      setError(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  // Helper for formatting date in the dropdown
  const formatUploadDate = (dateString) => {
    return new Date(dateString).toLocaleString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-dark-900">Your Dashboard</h2>
        <button
          onClick={handleLogout}
          className="text-gray-500 hover:text-ocean-blue text-sm font-medium"
        >
          Logout
        </button>
      </div>

      {/* Analysis Form Card */}
      <div className="bg-white shadow-xl rounded-lg p-6 md:p-8 mb-10">
        <form onSubmit={handleSubmitAnalysis} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* --- RESUME SOURCE SECTION --- */}
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-2">
                1. Select Your Resume
              </label>
              {/* Tabs for Upload vs Existing */}
              <div className="flex mb-2 rounded-md bg-gray-100 p-1">
                <button
                  type="button"
                  onClick={() => setResumeSourceTab("upload")}
                  className={`w-1/2 py-2 rounded-md text-sm font-medium ${
                    resumeSourceTab === "upload"
                      ? "bg-white shadow"
                      : "text-gray-500"
                  }`}
                >
                  Upload New
                </button>
                <button
                  type="button"
                  onClick={() => setResumeSourceTab("existing")}
                  disabled={resumeHistory.length === 0}
                  className={`w-1/2 py-2 rounded-md text-sm font-medium ${
                    resumeSourceTab === "existing"
                      ? "bg-white shadow"
                      : "text-gray-500"
                  } ${
                    resumeHistory.length === 0
                      ? "opacity-50 cursor-not-allowed"
                      : ""
                  }`}
                >
                  Use Existing
                </button>
              </div>

              {/* Tab Content */}
              <div>
                {resumeSourceTab === "upload" && (
                  <input
                    id="resume-upload"
                    type="file"
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-500 mt-2
                               file:mr-4 file:py-2 file:px-4
                               file:rounded-md file:border-0
                               file:text-sm file:font-semibold
                               file:bg-ocean-blue file:text-white
                               hover:file:bg-royal-purple"
                  />
                )}
                {resumeSourceTab === "existing" && (
                  <select
                    id="resume-select"
                    value={selectedResumeId}
                    onChange={(e) => setSelectedResumeId(e.target.value)}
                    className="block w-full mt-2 px-3 py-2 border border-gray-300 rounded-md shadow-sm
                               focus:outline-none focus:ring-ocean-blue focus:border-ocean-blue sm:text-sm"
                  >
                    {resumeHistory.map((resume) => (
                      <option key={resume.id} value={resume.id}>
                        {resume.original_filename} (
                        {formatUploadDate(resume.uploaded_at)})
                      </option>
                    ))}
                  </select>
                )}
              </div>
            </div>

            {/* --- OTHER FORM INPUTS --- */}
            <div>
              <label
                htmlFor="role-name"
                className="block text-sm font-medium text-gray-500 mb-2"
              >
                2. Enter Target Role
              </label>
              <input
                id="role-name"
                type="text"
                value={roleName}
                onChange={(e) => setRoleName(e.target.value)}
                required
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                           focus:outline-none focus:ring-ocean-blue focus:border-ocean-blue sm:text-sm"
              />
            </div>

            <div>
              <label
                htmlFor="learning-pref"
                className="block text-sm font-medium text-gray-500 mb-2"
              >
                3. Choose Learning Preference
              </label>
              <select
                id="learning-pref"
                value={learningPref}
                onChange={(e) => setLearningPref(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm
                           focus:outline-none focus:ring-ocean-blue focus:border-ocean-blue sm:text-sm"
              >
                <option>Coding Projects</option>
                <option>Video Courses</option>
                <option>Reading / Docs</option>
              </select>
            </div>
          </div>

          <div className="pt-4">
            <FormButton isLoading={isLoading} type="submit">
              {isLoading ? "Analyzing..." : "Start Analysis"}
            </FormButton>
          </div>
        </form>
      </div>

      {/* --- Loading and Error States --- */}
      {isLoading && (
        <div className="text-center py-10">
          <p className="text-lg text-ocean-blue font-semibold">
            Analyzing... (This may take up to 30 seconds)
          </p>
          <p className="text-gray-500">
            Generating your personalized career roadmap...
          </p>
        </div>
      )}
      {error && (
        <div className="bg-error-red bg-opacity-10 text-error-red border border-error-red rounded-md p-4 text-center">
          {error}
        </div>
      )}

      {/* --- Results Section --- */}
      {skillGapResult && !isLoading && (
        <div className="bg-white shadow-xl rounded-lg">
          {/* Tab Headers */}
          <div className="flex border-b border-gray-200">
            <button
              className={`py-4 px-6 font-medium text-sm ${
                activeTab === "skillGap"
                  ? "border-b-2 border-ocean-blue text-ocean-blue"
                  : "text-gray-500 hover:text-dark-700"
              }`}
              onClick={() => setActiveTab("skillGap")}
            >
              Skill Gap Report
            </button>
            <button
              className={`py-4 px-6 font-medium text-sm ${
                activeTab === "optimized"
                  ? "border-b-2 border-ocean-blue text-ocean-blue"
                  : "text-gray-500 hover:text-dark-700"
              }`}
              onClick={() => setActiveTab("optimized")}
            >
              Optimized Resume
            </button>
          </div>

          {/* Tab Content */}
          <div className="p-6 md:p-8">
            {activeTab === "skillGap" && (
              <SkillGapReport report={skillGapResult} />
            )}
            {activeTab === "optimized" && (
              <OptimizedResume resume={optimizedResumeResult} />
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
