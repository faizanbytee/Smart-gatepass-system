package com.niet.gatepass.controller;

import com.niet.gatepass.model.GatePass;
import com.niet.gatepass.model.PassStatus;
import com.niet.gatepass.repository.GatePassRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("/guard")
public class GuardController {

    @Autowired
    private GatePassRepository gatePassRepository;

    @GetMapping("/dashboard")
    public String dashboard(Model model, @RequestParam(value = "query", required = false) String query) {
        if (query != null && !query.trim().isEmpty()) {
            List<GatePass> searchResults = gatePassRepository.findActivePassesByStudentUsername(query.trim(), Arrays.asList(PassStatus.APPROVED, PassStatus.OUT));
            model.addAttribute("searchResults", searchResults);
            model.addAttribute("searchQuery", query);
        }
        
        List<GatePass> checkedOutPasses = gatePassRepository.findByStatusOrderByCreatedAtDesc(PassStatus.OUT);
        List<GatePass> recentlyReturned = gatePassRepository.findByStatusOrderByCreatedAtDesc(PassStatus.RETURNED);
        
        model.addAttribute("checkedOutPasses", checkedOutPasses);
        model.addAttribute("recentlyReturned", recentlyReturned.size() > 5 ? recentlyReturned.subList(0, 5) : recentlyReturned);
        return "guard/dashboard";
    }

    @PostMapping("/checkout")
    public String checkoutStudent(@RequestParam("passId") Long passId) {
        Optional<GatePass> passOpt = gatePassRepository.findById(passId);
        if (passOpt.isPresent()) {
            GatePass pass = passOpt.get();
            if (pass.getStatus() == PassStatus.APPROVED) {
                pass.setStatus(PassStatus.OUT);
                pass.setActualExitTime(LocalDateTime.now());
                gatePassRepository.save(pass);
            }
        }
        return "redirect:/guard/dashboard?success=Student checked out successfully";
    }

    @PostMapping("/checkin")
    public String checkinStudent(@RequestParam("passId") Long passId) {
        Optional<GatePass> passOpt = gatePassRepository.findById(passId);
        if (passOpt.isPresent()) {
            GatePass pass = passOpt.get();
            if (pass.getStatus() == PassStatus.OUT) {
                pass.setStatus(PassStatus.RETURNED);
                pass.setActualEntryTime(LocalDateTime.now());
                gatePassRepository.save(pass);
            }
        }
        return "redirect:/guard/dashboard?success=Student checked in successfully";
    }
}
