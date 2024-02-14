"use strict";(self.webpackChunk_coreui_coreui_free_react_admin_template=self.webpackChunk_coreui_coreui_free_react_admin_template||[]).push([[6657],{6657:(e,s,a)=>{a.r(s),a.d(s,{default:()=>m});var l=a(2791),r=a(6912),n=a(2937),d=(a(2673),a(9792)),c=a(5294),t=a(2958),i=a(2585),o=a(7689),g=a(184);const m=()=>{const e=new URL(window.location.href.replace("/#","")),[s]=(0,l.useState)(e.searchParams.get("slug")),[a,m]=(0,l.useState)(null),[x,h]=(0,l.useState)(null),{state:u,dispatch:j}=(0,l.useContext)(i.y),{accessToken:b}=u,p=(0,l.useRef)(null),[N,y]=(0,l.useState)(!1),v=(0,l.useRef)(null),f=(0,o.s0)(),[w,k]=(0,d.Z)();(0,l.useEffect)((()=>{if(s){const e={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},a=c.Z.create();k(w,a,"/manage/session/create_lecture_session/","post",e,{lecture_slug:s},null).then((e=>{if(!1===e.error){const s=e.response;v.current||(v.current=new WebSocket("".concat(t.I,"/ws/attendance_session/").concat(s.data.data.session_id,"/?").concat(b))),h(s.data.data.marked_attendances),m(s.data.data)}else alert(e.errorMessage.message),f("/teacher/dashboard")}))}}),[s]),(0,l.useEffect)((()=>{v.current&&(v.current.onopen=()=>{console.log("WebSocket connection established")},v.current.onclose=()=>{console.log("WebSocket connection closed")},v.current.onmessage=e=>{let s=JSON.parse(e.data);console.log(s),s.message&&("attendance_marked"==s.message.action?h((e=>[...e,s.message.data])):"session_ended"==s.message.action?(h(s.message.data.marked_attendances),alert("Session has ended"),y(!0)):"session_already_ended"==s.message.action&&alert("Session has already been ended"))},v.current.onerror=e=>{console.error("WebSocket error:",e)})}),[v.current]);return(0,g.jsx)(g.Fragment,{children:a?(0,g.jsxs)(g.Fragment,{children:[(0,g.jsx)(n.rb,{children:(0,g.jsx)(n.b7,{children:(0,g.jsxs)(n.xH,{className:"card",children:[(0,g.jsx)(n.bn,{children:(0,g.jsxs)("div",{className:"d-flex justify-content-sm-between justify-content-center flex-wrap",children:[(0,g.jsx)("div",{className:"mx-3 mb-2",children:(0,g.jsx)("strong",{children:"Lecture Details"})}),(0,g.jsx)("div",{className:"mx-3",children:(0,g.jsx)("strong",{children:new Date(a.created_at).toLocaleString()})})]})}),(0,g.jsx)(n.sl,{children:(0,g.jsx)("div",{className:"d-flex flex-wrap w-100",children:(0,g.jsx)("div",{className:"col-12",children:(0,g.jsxs)("div",{className:"w-100 d-flex flex-wrap flex-1 justify-center",children:[(0,g.jsx)("div",{className:"text-center col-12 col-sm-3 col-md-3 col-lg-3",children:(0,g.jsxs)("p",{style:{margin:"0px",padding:"0px"},children:[a.lecture.start_time," | ",a.lecture.end_time]})}),(0,g.jsx)("div",{className:"text-center col-12 col-sm-3 col-md-3 col-lg-3",children:(0,g.jsx)("p",{style:{margin:"0px",padding:"0px"},children:a.lecture.subject.subject_name})}),(0,g.jsx)("div",{className:"text-center col-12 col-sm-3 col-md-3 col-lg-3",children:(0,g.jsx)("p",{style:{margin:"0px",padding:"0px"},children:a.lecture.type})}),(0,g.jsx)("div",{className:"text-center col-12 col-sm-3 col-md-3 col-lg-3",children:(0,g.jsx)("p",{style:{margin:"0px",padding:"0px"},children:a.lecture.classroom.class_name})})]})})})})]})})}),(0,g.jsx)(n.rb,{className:"mt-3",children:(0,g.jsx)(n.b7,{xs:!0,children:(0,g.jsxs)(n.xH,{className:"mb-4",children:[(0,g.jsx)(n.bn,{className:"",children:N?(0,g.jsx)(r.DownloadTableExcel,{filename:"".concat(a.lecture.subject.subject_name," - ").concat(new Date(a.lecture.session.day).toLocaleString()),sheet:"users",currentTableRef:p.current,children:(0,g.jsx)("button",{className:"my-2 w-100 btn btn btn-outline-primary",children:" Export excel "})}):(0,g.jsxs)("div",{className:"my-2 w-100 btn btn btn-outline-danger",onClick:()=>{v.current&&v.current.send(JSON.stringify({action:"end_session"}))},children:[(0,g.jsx)("span",{className:"me-3 d-inline",children:"End Session"}),(0,g.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"d-inline bi bi-stop-circle-fill",viewBox:"0 0 16 16",children:(0,g.jsx)("path",{d:"M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M6.5 5A1.5 1.5 0 0 0 5 6.5v3A1.5 1.5 0 0 0 6.5 11h3A1.5 1.5 0 0 0 11 9.5v-3A1.5 1.5 0 0 0 9.5 5z"})})]})}),(0,g.jsx)(n.sl,{children:(0,g.jsx)(n.rb,{className:"w-100 flex-col",children:(0,g.jsx)(n.b7,{className:"col-12",children:(0,g.jsx)("div",{className:"table-responsive",children:(0,g.jsxs)("table",{align:"middle",className:"table align-middle table-hover text-center mb-0 border hover responsive",ref:p,children:[(0,g.jsxs)(n.V,{color:"light",children:[(0,g.jsx)(n.T6,{"aria-colspan":5,children:(0,g.jsx)(n.is,{colSpan:5,children:"L.D COLLEGE OF ENGINEERING"})}),(0,g.jsx)(n.T6,{"aria-colspan":5,children:(0,g.jsxs)(n.is,{colSpan:5,children:["Subject: ",a.lecture.subject.subject_name," | DATE: ",a.lecture.session.day]})}),(0,g.jsxs)(n.T6,{children:[(0,g.jsx)(n.is,{children:"Enrollment No"}),(0,g.jsx)(n.is,{children:"Student Name"}),(0,g.jsx)(n.is,{children:"IP Addr"}),(0,g.jsx)(n.is,{children:"Batch"}),(0,g.jsx)(n.is,{children:"Status"})]})]}),(0,g.jsx)(n.NR,{children:x&&x.map(((e,s)=>(0,g.jsxs)(n.T6,{"v-for":"alert alert-primary item in tableItems",children:[(0,g.jsx)(n.NN,{children:(0,g.jsx)("div",{children:e.student.enrollment?e.student.enrollment:"-"})}),(0,g.jsx)(n.NN,{children:(0,g.jsx)("div",{children:e.student.profile.name?e.student.profile.name:"-"})}),(0,g.jsx)(n.NN,{children:(0,g.jsx)("div",{children:e.marking_ip?e.marking_ip:"-"})}),(0,g.jsx)(n.NN,{children:(0,g.jsx)("div",{children:e.batches?e.batches.map(((e,s)=>(0,g.jsx)("span",{children:e.batch_name.toUpperCase()},s))):"-"})}),e.is_present?(0,g.jsx)(n.NN,{children:(0,g.jsxs)("div",{className:"text-success d-flex align-items-center justify-content-center",children:[(0,g.jsxs)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"mx-auto bi bi-patch-check",viewBox:"0 0 16 16",children:[(0,g.jsx)("path",{fillRule:"evenodd",d:"M10.354 6.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7 8.793l2.646-2.647a.5.5 0 0 1 .708 0"}),(0,g.jsx)("path",{d:"m10.273 2.513-.921-.944.715-.698.622.637.89-.011a2.89 2.89 0 0 1 2.924 2.924l-.01.89.636.622a2.89 2.89 0 0 1 0 4.134l-.637.622.011.89a2.89 2.89 0 0 1-2.924 2.924l-.89-.01-.622.636a2.89 2.89 0 0 1-4.134 0l-.622-.637-.89.011a2.89 2.89 0 0 1-2.924-2.924l.01-.89-.636-.622a2.89 2.89 0 0 1 0-4.134l.637-.622-.011-.89a2.89 2.89 0 0 1 2.924-2.924l.89.01.622-.636a2.89 2.89 0 0 1 4.134 0l-.715.698a1.89 1.89 0 0 0-2.704 0l-.92.944-1.32-.016a1.89 1.89 0 0 0-1.911 1.912l.016 1.318-.944.921a1.89 1.89 0 0 0 0 2.704l.944.92-.016 1.32a1.89 1.89 0 0 0 1.912 1.911l1.318-.016.921.944a1.89 1.89 0 0 0 2.704 0l.92-.944 1.32.016a1.89 1.89 0 0 0 1.911-1.912l-.016-1.318.944-.921a1.89 1.89 0 0 0 0-2.704l-.944-.92.016-1.32a1.89 1.89 0 0 0-1.912-1.911z"})]}),(0,g.jsx)("p",{style:{visibility:"hidden"},children:"P"})]})}):(0,g.jsx)(n.NN,{children:(0,g.jsxs)("div",{className:"text-danger d-flex align-items-center justify-content-center",children:[(0,g.jsxs)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"bi bi-x-octagon",viewBox:"0 0 16 16",children:[(0,g.jsx)("path",{d:"M4.54.146A.5.5 0 0 1 4.893 0h6.214a.5.5 0 0 1 .353.146l4.394 4.394a.5.5 0 0 1 .146.353v6.214a.5.5 0 0 1-.146.353l-4.394 4.394a.5.5 0 0 1-.353.146H4.893a.5.5 0 0 1-.353-.146L.146 11.46A.5.5 0 0 1 0 11.107V4.893a.5.5 0 0 1 .146-.353zM5.1 1 1 5.1v5.8L5.1 15h5.8l4.1-4.1V5.1L10.9 1z"}),(0,g.jsx)("path",{d:"M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"})]}),(0,g.jsx)("p",{style:{visibility:"hidden"},children:"F"})]})})]},s)))})]})})})})})]})})})]}):(0,g.jsxs)(g.Fragment,{children:[(0,g.jsxs)("div",{role:"status",className:"p-4 border border-gray-200 rounded shadow animate-pulse md:p-6 dark:border-gray-700",children:[(0,g.jsx)("div",{className:"h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-32 mb-2.5"}),(0,g.jsx)("div",{className:"w-48 h-2 mb-10 bg-gray-200 rounded-full dark:bg-gray-700"}),(0,g.jsxs)("div",{className:"flex items-baseline mt-4",children:[(0,g.jsx)("div",{className:"w-full bg-gray-200 rounded-t-lg h-72 dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full h-56 ms-6 bg-gray-200 rounded-t-lg dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full bg-gray-200 rounded-t-lg h-72 ms-6 dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full h-64 ms-6 bg-gray-200 rounded-t-lg dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full bg-gray-200 rounded-t-lg h-80 ms-6 dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full bg-gray-200 rounded-t-lg h-72 ms-6 dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full bg-gray-200 rounded-t-lg h-80 ms-6 dark:bg-gray-300"})]}),(0,g.jsx)("span",{className:"sr-only",children:"Loading..."})]}),(0,g.jsxs)("div",{role:"status",className:"p-4 border border-gray-200 rounded shadow animate-pulse md:p-6 dark:border-gray-700",children:[(0,g.jsx)("div",{className:"h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-32 mb-2.5"}),(0,g.jsx)("div",{className:"w-48 h-2 mb-10 bg-gray-200 rounded-full dark:bg-gray-700"}),(0,g.jsxs)("div",{className:"flex items-baseline mt-4",children:[(0,g.jsx)("div",{className:"w-full bg-gray-200 rounded-t-lg h-72 dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full h-56 ms-6 bg-gray-200 rounded-t-lg dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full bg-gray-200 rounded-t-lg h-72 ms-6 dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full h-64 ms-6 bg-gray-200 rounded-t-lg dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full bg-gray-200 rounded-t-lg h-80 ms-6 dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full bg-gray-200 rounded-t-lg h-72 ms-6 dark:bg-gray-300"}),(0,g.jsx)("div",{className:"w-full bg-gray-200 rounded-t-lg h-80 ms-6 dark:bg-gray-300"})]}),(0,g.jsx)("span",{className:"sr-only",children:"Loading..."})]})]})})}}}]);
//# sourceMappingURL=6657.b618b35c.chunk.js.map