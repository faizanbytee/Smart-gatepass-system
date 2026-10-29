package com.niet.gatepass.controller;

import com.niet.gatepass.model.GatePass;
import com.niet.gatepass.model.PassStatus;
import com.niet.gatepass.model.User;
import com.niet.gatepass.repository.GatePassRepository;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("/warden")
public class WardenController {

    @Autowired
    private GatePassRepository gatePassRepository;

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        List<GatePass> pendingPasses = gatePassRepository.findByStatusOrderByCreatedAtDesc(PassStatus.PENDING);
        List<GatePass> historyPasses = gatePassRepository.findByStatusNotOrderByCreatedAtDesc(PassStatus.PENDING);
        
        long pendingCount = pendingPasses.size();
        long activeOutCount = gatePassRepository.findByStatusOrderByCreatedAtDesc(PassStatus.OUT).size();
        long totalProcessed = historyPasses.size();

        model.addAttribute("pendingPasses", pendingPasses);
        model.addAttribute("historyPasses", historyPasses);
        model.addAttribute("pendingCount", pendingCount);
        model.addAttribute("activeOutCount", activeOutCount);
        model.addAttribute("totalProcessed", totalProcessed);
        
        return "warden/dashboard";
    }

    @PostMapping("/approve")
    public String approvePass(@RequestParam("passId") Long passId,
                              @RequestParam(value = "remarks", defaultValue = "") String remarks,
                              HttpSession session) {
        User warden = (User) session.getAttribute("user");
        Optional<GatePass> passOpt = gatePassRepository.findById(passId);
        
        if (passOpt.isPresent()) {
            GatePass pass = passOpt.get();
            if (pass.getStatus() == PassStatus.PENDING) {
                pass.setStatus(PassStatus.APPROVED);
                pass.setApprovedBy(warden);
                pass.setRemarks(remarks);
                gatePassRepository.save(pass);
            }
        }
        return "redirect:/warden/dashboard?success=Gate pass approved";
    }

    @PostMapping("/reject")
    public String rejectPass(@RequestParam("passId") Long passId,
                             @RequestParam(value = "remarks", defaultValue = "") String remarks,
                             HttpSession session) {
        User warden = (User) session.getAttribute("user");
        Optional<GatePass> passOpt = gatePassRepository.findById(passId);
        
        if (passOpt.isPresent()) {
            GatePass pass = passOpt.get();
            if (pass.getStatus() == PassStatus.PENDING) {
                pass.setStatus(PassStatus.REJECTED);
                pass.setApprovedBy(warden);
                pass.setRemarks(remarks);
                gatePassRepository.save(pass);
            }
        }
        return "redirect:/warden/dashboard?success=Gate pass rejected";
    }
}
