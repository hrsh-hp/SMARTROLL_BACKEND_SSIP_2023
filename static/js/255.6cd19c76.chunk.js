"use strict";(self.webpackChunk_coreui_coreui_free_react_admin_template=self.webpackChunk_coreui_coreui_free_react_admin_template||[]).push([[255],{3255:(e,s,t)=>{t.r(s),t.d(s,{default:()=>u});var n=t(2791),i=t(5294),r=t(2585),a=t(2937),l=t(3645),o=t(7689),c=t(9792),d=t(184);const h=(e,s,t)=>{const[h,u]=(0,c.Z)(),[x,m]=(0,n.useState)(!1),[g,j]=(0,n.useState)(null),{state:p,dispatch:b}=(0,n.useContext)(r.y),{accessToken:v,refreshToken:_,semesters:f,objectCount:k}=p,[y,C]=(0,n.useState)(k);(0,o.s0)();return(0,d.jsxs)(a.lx,{className:"row g-3 needs-validation",noValidate:!0,validated:x,onSubmit:n=>{!1===n.currentTarget.checkValidity()&&(n.preventDefault(),n.stopPropagation()),n.preventDefault(),m(!0);(async s=>{if(g){const n={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},r=i.Z.create();let a="/manage/add_division/",o="post",c=n,d=await u(h,r,a,o,c,s,null);if(0==d.error){let s=d.response,n={...k};n.divisons+=1,b({type:"GET_OBJECTS",payload:n}),e((e=>[...e,s.data.data])),t((e=>e+1)),(0,l.w)("success","Semester Added successfully...!")}else alert(d.errorMessage.message)}else alert("Please Enter The Valid Division Name")})({division_name:g,semester_slug:s})},children:[(0,d.jsxs)(a.b7,{md:12,children:[(0,d.jsx)(a.L8,{htmlFor:"validationCustom01",children:"Division Name"}),(0,d.jsx)(a.jO,{type:"text",id:"validationCustom01",onChange:e=>j(e.target.value.toUpperCase()),required:!0,maxLength:1}),(0,d.jsx)(a.CO,{valid:!0,children:"Looks good!"})]}),(0,d.jsx)(a.b7,{xs:12,children:(0,d.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})},u=e=>{const{semester_slug:s,chageSteps:t,set_division_slug:c,set_divisionCount:u}=e,[x,m]=(0,n.useState)([]),{state:g,dispatch:j}=(0,n.useContext)(r.y),{accessToken:p,refreshToken:b,semesters:v}=g;(0,o.s0)();return(0,n.useEffect)((()=>{(async()=>{const e=i.Z.create();let t={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},n=await(0,l.J)(e,"/manage/get_divisions","get",t,null,{semester_slug:s});if(0==n.error){let e=n.response;m(e.data.data)}else alert(n.errorMessage.message)})()}),[]),(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(a.rb,{children:(0,d.jsx)(a.b7,{xs:12,children:(0,d.jsxs)(a.xH,{className:"mb-3",children:[(0,d.jsx)(a.bn,{children:(0,d.jsx)("strong",{children:"Divison"})}),(0,d.jsx)(a.sl,{children:h(m,s,u)})]})})}),(0,d.jsx)(a.rb,{children:(0,d.jsx)(a.b7,{xs:!0,children:(0,d.jsxs)(a.xH,{className:"mb-4",children:[(0,d.jsx)(a.bn,{children:(0,d.jsx)("strong",{children:"Division History"})}),(0,d.jsx)(a.sl,{children:(0,d.jsxs)(a.Sx,{align:"middle",className:"mb-0 border",hover:!0,responsive:!0,children:[(0,d.jsx)(a.V,{color:"light",children:(0,d.jsx)(a.T6,{onClick:()=>{t("batch")},style:{textAlign:"center"},children:(0,d.jsx)(a.is,{children:"Division Name"})})}),(0,d.jsx)(a.NR,{style:{textAlign:"center"},children:x.map(((e,s)=>(0,d.jsx)(a.T6,{onClick:()=>{t("batch"),c(e.slug)},style:{cursor:"pointer"},children:(0,d.jsx)(a.NN,{children:(0,d.jsx)("div",{children:e.division_name})})},s)))})]})})]})})})]})}}}]);
//# sourceMappingURL=255.6cd19c76.chunk.js.map