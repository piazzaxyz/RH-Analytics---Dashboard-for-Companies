import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import DashboardLayout from "./components/layout/DashboardLayout";
import DashboardPage from "./pages/DashboardPage";
import EmployeesPage from "./pages/EmployeesPage";
import EvaluationsPage from "./pages/EvaluationsPage";
import LoansPage from "./pages/LoansPage";
import LoginPage from "./pages/LoginPage";
import PayrollPage from "./pages/PayrollPage";
import PositionsPage from "./pages/PositionsPage";
import TimesheetsPage from "./pages/TimesheetsPage";

function App() {
	return (
		<Routes>
			<Route path="/login" element={<LoginPage />} />
			<Route
				path="/"
				element={
					<ProtectedRoute>
						<DashboardLayout />
					</ProtectedRoute>
				}
			>
				<Route index element={<DashboardPage />} />
				<Route path="employees" element={<EmployeesPage />} />
				<Route path="timesheets" element={<TimesheetsPage />} />
				<Route path="payroll" element={<PayrollPage />} />
				<Route path="evaluations" element={<EvaluationsPage />} />
				<Route path="positions" element={<PositionsPage />} />
				<Route path="loans" element={<LoansPage />} />
			</Route>
			<Route path="*" element={<Navigate to="/" replace />} />
		</Routes>
	);
}

export default App;
