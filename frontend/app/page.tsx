"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { 
  LayoutGrid, PieChart, BrainCircuit, Settings, Search, Bell, 
  TrendingDown, TrendingUp, ChevronDown, ChevronLeft, ChevronRight, Lock, ArrowDown, ArrowUp,
  Lightbulb
} from "lucide-react";
import { 
  AreaChart, Area, ResponsiveContainer, Tooltip, YAxis, XAxis, ReferenceLine, CartesianGrid 
} from "recharts";

export default function FinSightsDashboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(""); 
  const [isSearching, setIsSearching] = useState(false); 
  const [activeSymbol, setActiveSymbol] = useState(""); 

  const [chartData] = useState(Array.from({ length: 60 }, (_, i) => ({
    time: ["09:15", "10:30", "11:45", "01:00", "02:15", "03:30"][Math.floor(i/10)] || "03:30",
    value: 24230 - (i * 4) + (Math.sin(i / 2) * 20) + (Math.random() * 15)
  })));

  const fetchMarketData = async (symbol: string = "") => {
    try {
      if (symbol) {
        setIsSearching(true);
        setData(null); 
      }
      setActiveSymbol(symbol); 
      
      
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      let url = symbol 
        ? `${baseUrl}/api/search?symbol=${symbol}` 
        : `${baseUrl}/api/market-analysis`;
      
      const res = await axios.get(url);
      setData(res.data);
    } catch (err) {
      console.error("Fetch error:", err);
    } finally {
      setLoading(false);
      setIsSearching(false);
    }
  };

  useEffect(() => {
    fetchMarketData(); 
    const intervalId = setInterval(() => {
      setActiveSymbol((current) => {
        fetchMarketData(current);
        return current;
      });
    }, 30000);
    return () => clearInterval(intervalId);
  }, []); 

  const handleSearch = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && searchQuery.trim() !== "") {
      fetchMarketData(searchQuery.trim());
    }
  };

  if (loading) return <div className="h-screen bg-[#020817] flex items-center justify-center text-blue-500 animate-pulse text-base font-bold font-['Inter',sans-serif] tracking-[0.2em]">FINSIGHTS AI INITIALIZING...</div>;

  const mainStock = data?.main_stock;
  const isDown = parseFloat(mainStock?.change) < 0;

  return (
    <div className="flex h-screen bg-[#020817] text-slate-300 font-['Inter',sans-serif] overflow-hidden">
      
      {/* Sidebar */}
      <aside className="w-64 border-r border-blue-500/10 p-8 flex flex-col relative">
        <div className="absolute top-0 right-0 w-[1.5px] h-full bg-gradient-to-b from-transparent via-blue-500/50 to-transparent shadow-[0_0_20px_rgba(59,130,246,0.6)]"></div>
        <div className="flex items-center gap-3 mb-12">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-400 to-blue-700 flex items-center justify-center shadow-lg shadow-blue-600/40">
            <TrendingUp size={20} className="text-white"/>
          </div>
          <span className="text-xl font-bold text-white">FinSights <span className="text-blue-500">AI</span></span>
        </div>

        <nav className="space-y-4 flex-1">
          <NavItem icon={<LayoutGrid size={20}/>} label="Dashboard" active />
          <NavItem icon={<PieChart size={20}/>} label="Portfolio" />
          <NavItem icon={<BrainCircuit size={20}/>} label="AI Analysis" />
          <NavItem icon={<Settings size={20}/>} label="Settings" />
        </nav>

        <div className="mt-auto space-y-2.5">
          <div className="flex items-center gap-2 text-emerald-400 text-xs font-semibold">
            <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.8)] animate-pulse"></div> Market is Open
          </div>
          <div className="text-2xl font-bold text-white">09:35:42 AM</div>
          <div className="text-xs text-slate-500 font-normal">23 May 2025, Friday</div>
        </div>
      </aside>

      <div className="flex-1 flex flex-col px-10 py-8 overflow-y-auto relative">
        
        {isSearching && (
             <div className="absolute inset-0 bg-[#020817]/60 backdrop-blur-sm z-50 flex items-center justify-center rounded-3xl">
                 <div className="text-blue-500 animate-pulse text-sm font-bold tracking-[0.2em]">ANALYZING {searchQuery.toUpperCase()}...</div>
             </div>
        )}

        {/* Header */}
        <header className="flex justify-between items-center mb-8">
          <div className="flex items-center bg-slate-900/50 border border-white/5 rounded-xl px-5 py-3 w-[450px] shadow-inner focus-within:border-blue-500/50 transition-colors">
            <Search size={18} className="text-slate-500" />
            <input 
              className="bg-transparent outline-none ml-3 w-full text-sm text-white placeholder:text-slate-500 font-normal" 
              placeholder="Enter symbol (e.g. RELIANCE) and press Enter..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={handleSearch}
            />
            <span className="text-xs bg-slate-800/80 px-2 py-0.5 rounded text-slate-500 border border-slate-700 font-mono">↵</span>
          </div>
          <div className="flex items-center gap-6">
            <Bell size={20} className="text-slate-500 hover:text-white cursor-pointer transition-colors" />
            <div className="flex items-center gap-3 bg-slate-900/40 p-1.5 pr-4 rounded-xl border border-white/5 hover:border-white/10 transition-all cursor-pointer">
              <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-blue-400 font-bold text-sm shadow-inner">B</div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-white">Bhumika</span>
                <ChevronDown size={14} className="text-slate-500" />
              </div>
            </div>
          </div>
        </header>

        {/* Top Info Cards */}
        <div className="grid grid-cols-12 gap-6 mb-8">
          <div className="col-span-5 bg-[#0A101F] border border-white/5 p-8 rounded-3xl shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xs text-slate-500 font-semibold uppercase tracking-wider">{mainStock?.name || "NIFTY 50 INDEX"}</h2>
              <div className={`flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold border ${isDown ? 'bg-red-500/10 text-red-500 border-red-500/20' : 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20'}`}>
                {isDown ? <ArrowDown size={14} fill="currentColor"/> : <ArrowUp size={14} fill="currentColor"/>} 
                {Math.abs(parseFloat(mainStock?.change || "0"))}% {isDown ? 'down' : 'up'}
              </div>
            </div>
            <h1 className="text-5xl font-bold text-white tracking-tight">
              ₹ {mainStock?.price ? mainStock.price.toLocaleString() : "---"}
            </h1>
            <p className="text-xs text-slate-500 mt-3 font-normal">As of 23 May 2025, 09:35 AM IST</p>
          </div>
          
          <div className="col-span-7 grid grid-cols-3 gap-5">
            <MetricBox label="Open" val={mainStock?.open} icon={<Lock size={16} className="text-emerald-500"/>} />
            <MetricBox label="High" val={mainStock?.high} icon={<TrendingUp size={16} className="text-blue-500"/>} />
            <MetricBox label="Low" val={mainStock?.low} icon={<TrendingDown size={16} className="text-red-500"/>} />
          </div>
        </div>

        {/* Mid Section - AI Sentiment & Chart */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
          
          {/* Sentiment Report */}
          <div className="bg-[#0A1122] border border-blue-600/30 p-8 rounded-3xl shadow-[0_0_40px_rgba(37,99,235,0.08)] relative">
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center gap-3">
                <div className="p-2.5 bg-blue-600/20 rounded-xl border border-blue-500/30 text-blue-400"><BrainCircuit size={22}/></div>
                <h3 className="text-base font-semibold text-white">Groq AI Sentiment Report</h3>
              </div>
              <div className="flex gap-2">
                <span className="text-xs bg-blue-500/10 px-3 py-1.5 rounded-full text-blue-400 font-medium border border-blue-500/20 flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div> Neutral
                </span>
                <span className="text-xs bg-emerald-500/10 px-3 py-1.5 rounded-full text-emerald-400 font-medium border border-emerald-500/20">
                  Accuracy: {mainStock?.accuracy || 'Analyzing...'}
                </span>
              </div>
            </div>

            <h4 className="text-blue-400 text-sm font-semibold mb-3">Outlook for {mainStock?.name || "Market"}</h4>
            <p className="text-slate-400 text-sm font-normal leading-relaxed mb-6">
              {mainStock?.analysis || "Fetching latest market sentiment..."}
            </p>
            
            <div className="grid grid-cols-2 gap-8 mb-8">
              <AIList title="Key Drivers" items={['Global market uncertainty', 'FII selling pressure', 'Sectoral momentum']} />
              <AIList title="What to Watch" items={['Key resistance levels', 'Immediate support', 'Upcoming macroeconomic data']} />
            </div>

            {/* AI RECOMMENDATION BOX */}
            <div className="bg-blue-600/10 border border-blue-500/20 rounded-2xl p-5 mt-4">
              <div className="flex items-center gap-3 mb-2 text-blue-400">
                <Lightbulb size={18} className="animate-pulse" />
                <span className="text-xs font-bold uppercase tracking-widest">AI Recommendation</span>
              </div>
              <p className="text-sm font-bold text-white">
                {mainStock?.investment_advice || "Waiting for analysis..."}
              </p>
            </div>
          </div>

          {/* Intraday Chart */}
          <div className="bg-[#0A101F] border border-white/5 p-8 rounded-3xl shadow-xl">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-sm font-semibold text-white uppercase tracking-wider">{mainStock?.name || "NIFTY 50"} – <span className="text-slate-500">Intraday Trend</span></h3>
              <div className="flex gap-1 bg-slate-900/80 p-1 rounded-lg border border-white/5">
                {['1D', '1W', '1M', '3M', '1Y'].map(t => <span key={t} className={`px-3 py-1.5 rounded-md text-xs font-medium cursor-pointer transition-all ${t==='1D'?'bg-blue-600 text-white':'text-slate-500 hover:text-white'}`}>{t}</span>)}
              </div>
            </div>
            
            <div className="h-[220px] w-full relative">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorVal" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} opacity={0.3}/>
                  <XAxis hide />
                  <YAxis orientation="right" domain={['dataMin - 50', 'dataMax + 50']} tick={{fill: '#475569', fontSize: 12}} axisLine={false} tickLine={false} />
                  {/* ✅ FIX 2: Removed hardcoded 23997.55 from ReferenceLine */}
                  {mainStock?.price && (
                    <ReferenceLine y={mainStock.price} stroke={isDown ? "#ef4444" : "#10b981"} strokeDasharray="4 4" opacity={0.8}/>
                  )}
                  <Area type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorVal)" />
                  <Tooltip content={<CustomTooltip />} />
                </AreaChart>
              </ResponsiveContainer>
              <div className={`absolute right-0 bottom-[10%] text-xs font-bold px-2 py-1 rounded shadow-lg text-white ${isDown ? 'bg-red-600/90' : 'bg-emerald-600/90'}`}>
                ₹{mainStock?.price || "---"}
              </div>
            </div>
          </div>
        </div>

        {/* Market Movers */}
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Market Movers</h3>
        </div>
        
        <div className="grid grid-cols-5 gap-5">
          {data?.movers?.slice(0, 5).map((stock: any, i: number) => (
            <div key={i} className="bg-[#0A101F] border border-white/5 p-6 rounded-3xl hover:bg-slate-900/50 transition-all shadow-md">
              <div className="flex justify-between items-start mb-4">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">{stock.symbol}</p>
                <div className="w-12 h-6 overflow-hidden">
                  <ResponsiveContainer><AreaChart data={Array.from({length:6},()=>({v:Math.random()}))}><Area type="monotone" dataKey="v" stroke={stock.change<0?'#ef4444':'#10b981'} fill={stock.change<0?'#ef444420':'#10b98120'} strokeWidth={1.5} dot={false}/></AreaChart></ResponsiveContainer>
                </div>
              </div>
              <p className="text-lg font-semibold text-white mb-1">₹ {stock.price}</p>
              <p className={`text-xs font-semibold ${stock.change<0?'text-red-500':'text-emerald-500'}`}>{stock.change>0?'+':''}{stock.change}%</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-[#0f172a] border border-slate-700 px-3 py-2 rounded-lg shadow-xl">
        <p className="text-xs font-bold text-white">₹ {payload[0].value.toLocaleString()}</p>
      </div>
    );
  }
  return null;
};

const NavItem = ({ icon, label, active = false }: any) => (
  <div className={`flex items-center gap-4 px-5 py-3 rounded-2xl cursor-pointer transition-all ${active ? 'bg-blue-600/10 text-blue-400 border border-blue-500/20' : 'text-slate-500 hover:text-white hover:bg-white/5'}`}>
    <div className={`${active ? 'text-blue-400' : 'text-slate-500'}`}>{icon}</div> 
    <span className="text-sm font-medium">{label}</span>
  </div>
);

// at component level to avoid repetition and keep code clean
const MetricBox = ({ label, val, icon }: any) => (
  <div className="bg-[#0A101F] border border-white/5 p-6 rounded-3xl flex flex-col justify-between shadow-md">
    <div className="flex items-center gap-2 text-xs font-semibold uppercase text-slate-500 tracking-wider">{icon} {label}</div>
    <div className="text-xl font-semibold text-white mt-4 tracking-wide">
      ₹ {val ? val : "---"}
    </div>
  </div>
);

const AIList = ({ title, items }: any) => (
  <div>
    <p className="text-blue-400 font-semibold uppercase mb-3 text-xs tracking-wider">{title}</p>
    <ul className="space-y-2">
      {items.map((it: string) => (
        <li key={it} className="flex items-start gap-2 text-slate-400 font-normal text-sm leading-tight">
          <div className="w-1.5 h-1.5 rounded-full bg-blue-500/50 mt-1.5"></div> {it}
        </li>
      ))}
    </ul>
  </div>
);