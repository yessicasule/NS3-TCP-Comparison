/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * TCP Congestion Control Comparison
 * Compares TCP Reno vs NewReno vs Cubic
 * Author: NS-3 Project
 */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/traffic-control-module.h"
#include "ns3/flow-monitor-module.h"
#include <fstream>
#include <vector>
#include <map>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("TcpComparison");

// Global counters for throughput calculation
std::map<std::string, uint64_t> g_rxBytes;
std::map<std::string, uint64_t> g_lastRxBytes;

void
PrintProgress()
{
    NS_LOG_UNCOND("Simulation time: " << Simulator::Now().GetSeconds() << " seconds");
}

void
ReceivePacket(Ptr<const Packet> packet, const Address &from, const std::string &protocol)
{
    g_rxBytes[protocol] += packet->GetSize();
}

static void
CwndChange(std::string protocol, uint32_t oldcwnd, uint32_t newcwnd)
{
    NS_LOG_UNCOND(protocol << " time=" << Simulator::Now().GetSeconds()
                          << " cwnd=" << newcwnd);
}

static void
RtoChange(std::string protocol, Time oldRto, Time newRto)
{
    NS_LOG_UNCOND(protocol << " time=" << Simulator::Now().GetSeconds()
                          << " RTO=" << newRto.GetMilliSeconds() << "ms");
}

int
main(int argc, char *argv[])
{
    // Simulation parameters
    uint32_t nNodes = 10;                    // Number of nodes
    double simTime = 60.0;                   // Simulation time (seconds)
    uint32_t dataRate = 100;                 // Link bandwidth (Mbps)
    uint32_t delay = 10;                     // Link delay (ms)
    uint32_t maxBytes = 0;                   // Maximum bytes to send (0 = unlimited)
    bool enablePcap = true;                  // Enable PCAP tracing
    std::string transportProtocol = "TcpReno"; // Default protocol

    CommandLine cmd;
    cmd.AddValue("nNodes", "Number of nodes", nNodes);
    cmd.AddValue("simTime", "Simulation time (seconds)", simTime);
    cmd.AddValue("protocol", "TCP variant (TcpReno, TcpNewReno, TcpCubic)", transportProtocol);
    cmd.Parse(argc, argv);

    // 1. CREATE NODES
    NS_LOG_UNCOND("\n=== TCP CONGESTION CONTROL COMPARISON ===");
    NS_LOG_UNCOND("Creating " << nNodes << " nodes...");
    
    NodeContainer nodes;
    nodes.Create(nNodes);

    // 2. CREATE POINT-TO-POINT LINKS
    NS_LOG_UNCOND("Setting up point-to-point links...");
    
    PointToPointHelper pointToPoint;
    pointToPoint.SetDeviceAttribute("DataRate", DataRateValue(DataRate(dataRate * 1e6))); // Mbps
    pointToPoint.SetChannelAttribute("Delay", TimeValue(MilliSeconds(delay)));

    NetDeviceContainer devices;
    
    // Create links between nodes (star topology)
    for (uint32_t i = 1; i < nNodes; i++)
    {
        NetDeviceContainer link = pointToPoint.Install(nodes.Get(0), nodes.Get(i));
        devices.Add(link);
    }

    // 3. INSTALL INTERNET STACK
    NS_LOG_UNCOND("Installing Internet stack...");
    
    InternetStackHelper stack;
    
    // Configure TCP variant
    if (transportProtocol == "TcpReno")
    {
        Config::SetDefault("ns3::TcpL4Protocol::SocketType",
                          TypeIdValue(TcpReno::GetTypeId()));
    }
    else if (transportProtocol == "TcpNewReno")
    {
        Config::SetDefault("ns3::TcpL4Protocol::SocketType",
                          TypeIdValue(TcpNewReno::GetTypeId()));
    }
    else if (transportProtocol == "TcpCubic")
    {
        Config::SetDefault("ns3::TcpL4Protocol::SocketType",
                          TypeIdValue(TcpCubic::GetTypeId()));
    }
    
    stack.InstallAll();

    // 4. ASSIGN IP ADDRESSES
    NS_LOG_UNCOND("Assigning IP addresses...");
    
    Ipv4AddressHelper address;
    address.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces = address.Assign(devices);

    // 5. ENABLE ROUTING
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    // 6. CREATE APPLICATIONS (TCP BulkSend)
    NS_LOG_UNCOND("Creating TCP BulkSend applications...");
    
    // Server on node 0
    uint16_t sinkPort = 9;
    PacketSinkHelper packetSinkHelper("ns3::TcpSocketFactory",
                                     InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
    ApplicationContainer sinkApps = packetSinkHelper.Install(nodes.Get(0));
    sinkApps.Start(Seconds(0.0));
    sinkApps.Stop(Seconds(simTime));

    // Clients on nodes 1 to nNodes-1
    for (uint32_t i = 1; i < nNodes; i++)
    {
        BulkSendHelper source("ns3::TcpSocketFactory",
                             InetSocketAddress(interfaces.GetAddress(0), sinkPort));
        source.SetAttribute("MaxBytes", UintegerValue(maxBytes));
        source.SetAttribute("SendSize", UintegerValue(1448));
        
        ApplicationContainer sourceApps = source.Install(nodes.Get(i));
        sourceApps.Start(Seconds(0.0));
        sourceApps.Stop(Seconds(simTime));
    }

    // 7. CONNECT TRACE SOURCES (optional - for debugging)
    Config::ConnectWithoutContext(
        "/NodeList/*/ApplicationList/*/Socket/CongestionWindow",
        MakeCallback(&CwndChange, transportProtocol));

    // 8. PCAP TRACING
    if (enablePcap)
    {
        pointToPoint.EnablePcapAll(transportProtocol);
    }

    // 9. FLOW MONITOR
    NS_LOG_UNCOND("Setting up FlowMonitor...");
    
    Ptr<FlowMonitorHelper> flowmonHelper = CreateObject<FlowMonitorHelper>();
    FlowMonitorHelper::FlowStatsContainer stats = flowmonHelper->GetFlowStats();
    Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(
        flowmonHelper->GetClassifier());
    flowmonHelper->InstallAll();

    // 10. PERIODIC LOGGING
    NS_LOG_UNCOND("Starting simulation for " << simTime << " seconds...\n");
    
    Simulator::Schedule(Seconds(5.0), &PrintProgress);

    // 11. RUN SIMULATION
    Simulator::Stop(Seconds(simTime));
    Simulator::Run();

    // 12. COLLECT RESULTS
    NS_LOG_UNCOND("\n=== SIMULATION RESULTS ===");
    
    Ptr<FlowMonitor> monitor = flowmonHelper->GetMonitor();
    monitor->SerializeToXmlFile("flowmon-results.xml", true, true);

    int j = 0;
    float AvgThroughput = 0;
    float AvgDelay = 0;
    float AvgLoss = 0;
    float AvgPdr = 0;

    for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i =
             monitor->GetFlowStats().begin();
         i != monitor->GetFlowStats().end();
         ++i)
    {
        Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow(i->first);
        std::cout << "Flow " << i->first << " (" << t.sourceAddress << " -> "
                  << t.destinationAddress << ")\n";
        std::cout << "  Tx Packets = " << i->second.txPackets << "\n";
        std::cout << "  Rx Packets = " << i->second.rxPackets << "\n";
        std::cout << "  Throughput: "
                  << i->second.rxBytes * 8.0 /
                         (i->second.timeLastRxPacket.GetSeconds() -
                          i->second.timeFirstTxPacket.GetSeconds()) /
                         1024 / 1024
                  << " Mbps\n";

        std::cout << "  Mean Delay: "
                  << i->second.delaySum.GetSeconds() / i->second.rxPackets << "\n";
        std::cout << "  Mean Jitter: "
                  << i->second.jitterSum.GetSeconds() / (i->second.rxPackets - 1)
                  << "\n";

        float packetLossRatio =
            (i->second.txPackets - i->second.rxPackets) / static_cast<float>(i->second.txPackets);
        std::cout << "  Packet Loss Ratio: " << packetLossRatio << "\n";

        AvgThroughput += i->second.rxBytes * 8.0 /
                        (i->second.timeLastRxPacket.GetSeconds() -
                         i->second.timeFirstTxPacket.GetSeconds()) /
                        1024 / 1024;
        AvgDelay +=
            i->second.delaySum.GetSeconds() / i->second.rxPackets;
        AvgLoss += packetLossRatio;
        AvgPdr += (i->second.rxPackets / static_cast<float>(i->second.txPackets));
        j++;
    }

    AvgThroughput /= j;
    AvgDelay /= j;
    AvgLoss /= j;
    AvgPdr /= j;

    NS_LOG_UNCOND("\n=== AVERAGE METRICS FOR " << transportProtocol << " ===");
    NS_LOG_UNCOND("Average Throughput = " << AvgThroughput << " Mbps");
    NS_LOG_UNCOND("Average Delay = " << AvgDelay << " s");
    NS_LOG_UNCOND("Packet Loss Ratio = " << AvgLoss);
    NS_LOG_UNCOND("PDR = " << AvgPdr << " (" << AvgPdr * 100 << "%)");

    // Save to file
    std::ofstream outFile;
    outFile.open(transportProtocol + "-metrics.txt", std::ios_base::app);
    outFile << transportProtocol << "," << AvgThroughput << "," << AvgDelay << ","
            << AvgLoss << "," << AvgPdr << "\n";
    outFile.close();

    Simulator::Destroy();

    NS_LOG_UNCOND("\n=== SIMULATION COMPLETE ===");
    return 0;
}
