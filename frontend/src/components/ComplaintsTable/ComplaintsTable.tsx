// // src/components/ComplaintsTable/ComplaintsTable.tsx
// import React, { useEffect, useState } from 'react';
// import { fetchComplaints } from '../../services/api';

// interface Complaint {
//     id: string;
//     text: string;
//     prediction: string;
// }

// const ComplaintsTable: React.FC = () => {
//     const [complaints, setComplaints] = useState<Complaint[]>([]);

//     useEffect(() => {
//         fetchComplaints().then(setComplaints);
//     }, []);

//     return (
//         <div>
//             <h2>Complaints</h2>
//             <table>
//                 <thead>
//                     <tr>
//                         <th>ID</th>
//                         <th>Text</th>
//                         <th>Prediction</th>
//                     </tr>
//                 </thead>
//                 <tbody>
//                     {complaints.map((complaint) => (
//                         <tr key={complaint.id}>
//                             <td>{complaint.id}</td>
//                             <td>{complaint.text}</td>
//                             <td>{complaint.prediction}</td>
//                         </tr>
//                     ))}
//                 </tbody>
//             </table>
//         </div>
//     );
// };

// export default ComplaintsTable;
