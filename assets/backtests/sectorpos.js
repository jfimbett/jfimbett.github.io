if (chartColLabels === undefined) { var chartColLabels = {}; }
if (chartColLabels.exposureBreakdowns === undefined) {
    chartColLabels.exposureBreakdowns = {};
    chartColLabels.exposureBreakdowns.net = 'Net';
}

chartColLabels.exposureBreakdowns.fund = 'Fund';
chartColLabels.exposureBreakdowns.benchmark = 'Benchmark';


var tabsSectorLongDataTableHasRankOrder = false;
var tabsSectorLongChartType = 'bar';

var tabsSectorLongDataTable = [{"name" : "Apparel & Accessory Stores", "value": " 0" , "rank" : 1} ,{"name" : "Industrial Machinery & Equipment", "value": " 1" , "rank" : 2} ,{"name" : "Automative Dealers & Service Stations", "value": " 0" , "rank" : 3} ,{"name" : "Depository Institutions", "value": " 0" , "rank" : 4} ,{"name" : "Rubber & Miscellaneous Plastics Products", "value": " 1" , "rank" : 5} ,{"name" : "Stone, Clay, & Glass Products", "value": " 0" , "rank" : 6} ,{"name" : "Holding & Other Investment Offices", "value": " 1" , "rank" : 7} ,{"name" : "Transportation by Air", "value": " 0" , "rank" : 8} ,{"name" : "Business Services", "value": " 4" , "rank" : 9} ,{"name" : "Insurance Agents, Brokers, & Service", "value": " 0" , "rank" : 10} ,{"name" : "Oil & Gas Extraction", "value": " 2" , "rank" : 11} ,{"name" : "Food Stores", "value": " 0" , "rank" : 12} ,{"name" : "Insurance Carriers", "value": " 0" , "rank" : 13} ,{"name" : "Membership Organizations", "value": " 0" , "rank" : 14} ,{"name" : "Executive, Legislative, & General", "value": " 0" , "rank" : 15} ,{"name" : "Security & Commodity Brokers", "value": " 0" , "rank" : 16} ,{"name" : "Eating & Drinking Places", "value": " 0" , "rank" : 17} ,{"name" : "Building Materials & Gardening Supplies", "value": " 0" , "rank" : 18} ,{"name" : "Coal Mining", "value": " 0" , "rank" : 19} ,{"name" : "Chemical & Allied Products", "value": " 5" , "rank" : 20} ,{"name" : "Auto Repair, Services, & Parking", "value": " 0" , "rank" : 21} ,{"name" : "Apparel & Other Textile Products", "value": " 0" , "rank" : 22} ,{"name" : "Justice, Public Order, & Safety", "value": " 0" , "rank" : 23} ,{"name" : "Local & Interurban Passenger Transit", "value": " 0" , "rank" : 24} ,{"name" : "U.S. Postal Service", "value": " 0" , "rank" : 25} ,{"name" : "Electronic & Other Electric Equipment", "value": " 4" , "rank" : 26} ,{"name" : "Zoological Gardens", "value": " 0" , "rank" : 27} ,{"name" : "Educational Services", "value": " 0" , "rank" : 28} ,{"name" : "Miscellaneous Manufacturing Industries", "value": " 0" , "rank" : 29} ,{"name" : "Museums, Botanical, Zoological Gardens", "value": " 0" , "rank" : 30} ,{"name" : "Agricultural Services", "value": " 0" , "rank" : 31} ,{"name" : "Furniture & Fixtures", "value": " 0" , "rank" : 32} ,{"name" : "Environmental Quality & Housing", "value": " 0" , "rank" : 33} ,{"name" : "Miscellaneous Repair Services", "value": " 0" , "rank" : 34} ,{"name" : "Fabricated Metal Products", "value": " 0" , "rank" : 35} ,{"name" : "Wholesale Trade – Durable Goods", "value": " 0" , "rank" : 36} ,{"name" : "Miscellaneous Retail", "value": " 2" , "rank" : 37} ,{"name" : "Finance, Taxation, & Monetary Policy", "value": " 0" , "rank" : 38} ,{"name" : "Agricultural Production – Livestock", "value": " 0" , "rank" : 39} ,{"name" : "Metal, Mining", "value": " 0" , "rank" : 40} ,{"name" : "Printing & Publishing", "value": " 1" , "rank" : 41} ,{"name" : "Paper & Allied Products", "value": " 0" , "rank" : 42} ,{"name" : "Trucking & Warehousing", "value": " 0" , "rank" : 43} ,{"name" : "Engineering & Management Services", "value": " 1" , "rank" : 44} ,{"name" : "Amusement & Recreation Services", "value": " 0" , "rank" : 45} ,{"name" : "Heavy Construction, Except Building", "value": " 0" , "rank" : 46} ,{"name" : "Food & Kindred Products", "value": " 0" , "rank" : 47} ,{"name" : "Legal Services", "value": " 0" , "rank" : 48} ,{"name" : "Electric, Gas, & Sanitary Services", "value": " 2" , "rank" : 49} ,{"name" : "Water Transportation", "value": " 0" , "rank" : 50} ,{"name" : "Fishing, Hunting, & Trapping", "value": " 0" , "rank" : 51} ,{"name" : "Leather & Leather Products", "value": " 0" , "rank" : 52} ,{"name" : "Nondepository Institutions", "value": " 0" , "rank" : 53} ,{"name" : "Petroleum & Coal Products", "value": " 0" , "rank" : 54} ,{"name" : "Administration of Human Resources", "value": " 0" , "rank" : 55} ,{"name" : "Pipelines, Except Natural Gas", "value": " 0" , "rank" : 56} ,{"name" : "Furniture & Homefurnishings Stores", "value": " 0" , "rank" : 57} ,{"name" : "Hotels & Other Lodging Places", "value": " 0" , "rank" : 58} ,{"name" : "Tobacco Products", "value": " 0" , "rank" : 59} ,{"name" : "Instruments & Related Products", "value": " 0" , "rank" : 60} ,{"name" : "Private Households", "value": " 0" , "rank" : 61} ,{"name" : "Motion Pictures", "value": " 0" , "rank" : 62} ,{"name" : "Personal Services", "value": " 0" , "rank" : 63} ,{"name" : "Lumber & Wood Products", "value": " 0" , "rank" : 64} ,{"name" : "Forestry", "value": " 0" , "rank" : 65} ,{"name" : "Special Trade Contractors", "value": " 0" , "rank" : 66} ,{"name" : "Transportation Equipment", "value": " 0" , "rank" : 67} ,{"name" : "Agricultural Production – Crops", "value": " 0" , "rank" : 68} ,{"name" : "General Merchandise Stores", "value": " 0" , "rank" : 69} ,{"name" : "Textile Mill Products", "value": " 0" , "rank" : 70} ,{"name" : "Transportation Services", "value": " 0" , "rank" : 71} ,{"name" : "Social Services", "value": " 0" , "rank" : 72} ,{"name" : "Non-Classifiable Establishments", "value": " 0" , "rank" : 73} ,{"name" : "Services, Not Elsewhere Classified", "value": " 0" , "rank" : 74} ,{"name" : "Nonmetallic Minerals, Except Fuels", "value": " 0" , "rank" : 75} ,{"name" : "Health Services", "value": " 1" , "rank" : 76} ,{"name" : "Administration of Economic Programs", "value": " 0" , "rank" : 77} ,{"name" : "Wholesale Trade – Nondurable Goods", "value": " 0" , "rank" : 78} ,{"name" : "Primary Metal Industries", "value": " 0" , "rank" : 79} ,{"name" : "Railroad Transportation", "value": " 0" , "rank" : 80} ,{"name" : "Communications", "value": " 0" , "rank" : 81} ,{"name" : "General Building Contractors", "value": " 0" , "rank" : 82} ,{"name" : "Real Estate", "value": " 0" , "rank" : 83} ,{"name" : "National Security & International Affairs", "value": " 0" , "rank" : 84} ]
var tabsSectorLongDataChart = [{ "name": "fund", "index": 0, "legendIndex": 0, "data": [{ "name": "Information Technology", "y": 0.0, "rank": 0 }, { "name": "Health Care", "y": 0.0, "rank": 1 }, { "name": "Consumer Discretionary", "y": 0.0, "rank": 2 }, { "name": "Financials", "y": 0.0, "rank": 3 }, { "name": "Communication", "y": 0.0, "rank": 4 }, { "name": "Industrials", "y": 0.0, "rank": 5 }, { "name": "Consumer Staples", "y": 0.0, "rank": 6 }, { "name": "Energy", "y": 0.0, "rank": 7 }, { "name": "Materials", "y": 0.0, "rank": 8 }, { "name": "Utilities", "y": 0.0, "rank": 9 }, { "name": "Real Estate", "y": 0.0, "rank": 10 }, { "name": "Cash and/or Derivatives", "y": 0.0, "rank": 11 }] }];
tabsSectorLongDataChart = tabsSectorLongDataChart.filter(function(el) { return el != null; });
var tabsSectorLongHasPie = false;