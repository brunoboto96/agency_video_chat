import logo from "./logo.svg";
import "./App.css";

function App() {
  return (
    <div className="bg-[#282c34] h-screen">
      <img
        src={logo}
        className="w-[50px] h-[50px] mx-auto App-logo"
        alt="logo"
      />
      <hr className="border-2 border-blue-200 mx-10 my-5" />
      <div className="flex flex-col text-center space-y-5 justify-center my-5 rounded-md border-2 border-white mx-auto w-3/4 p-5">
        <h1 className="text-center text-white text-xl">Agency Info</h1>
        <small>
      Your agency information will be used to get 3 videos that align with your agency's brand and target audience.
        </small>
        <form className="flex flex-col space-y-5">
          {/* 
      agency_name
      agency_type
      industry
      location
      keywords
      target_audience
      */}
          <input
            type="text"
            placeholder="Agency Name"
            className="p-2 rounded-md border-2 border-white text-slate-600"
          />
          <input
            type="text"
            placeholder="Agency Type"
            className="p-2 rounded-md border-2 border-white text-slate-600"
          />
          <input
            type="text"
            placeholder="Industry"
            className="p-2 rounded-md border-2 border-white text-slate-600"
          />
          <input
            type="text"
            placeholder="Location"
            className="p-2 rounded-md border-2 border-white text-slate-600"
          />
          <input
            type="text"
            placeholder="Keywords"
            className="p-2 rounded-md border-2 border-white text-slate-600"
          />
          <input
            type="text"
            placeholder="Target Audience"
            className="p-2 rounded-md border-2 border-white text-slate-600"
          />

          <button className="p-2 bg-gray-500 hover:bg-gray-300 hover:text-slate-700 rounded-md text">
            <h1 className="text-center">Submit</h1>
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
