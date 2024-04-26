import { useContext } from "react";
import { Routes as Router, Route, Navigate, Outlet } from "react-router-dom";
import { AuthContext } from "./context/AuthContext";
import Login from "./components/Authorization/Login";
import Register from "./components/Authorization/Register";
import Home from "./components/Home/Home";

const PrivateRoutes = () => {
  const { authenticated } = useContext(AuthContext);
  console.log(authenticated);

  if (!authenticated) return <Navigate to="/login" replace />;

  return <Outlet />;
};

const Routes = () => {
  return (
    <Router>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<PrivateRoutes />}>
        <Route path="/" element={<Home />} />
      </Route>
    </Router>
  );
};

export default Routes;
