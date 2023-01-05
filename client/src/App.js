import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import ShowReport from './pages/show-report';
import Home from './pages/home';
import Report from './pages/report';
import Transaction from './pages/transaction';

export default function App() {
  return (
    <Router>
        <Routes>
            <Route path = '/show-report' element={<ShowReport />} />
            <Route path = "/" element={<Home />} />
            <Route path = "/report" element={<Report />} />
            <Route path = "/transaction" element={<Transaction />} />
        </Routes>
    </Router>
  );
}
