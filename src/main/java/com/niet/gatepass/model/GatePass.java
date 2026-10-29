package com.niet.gatepass.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "gate_passes")
public class GatePass {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "student_id", nullable = false)
    private User student;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private PassType passType;

    @Column(nullable = false)
    private String purpose;

    @Column(nullable = false)
    private String destination;

    @Column(nullable = false)
    private LocalDateTime departureDateTime;

    @Column(nullable = false)
    private LocalDateTime expectedReturnDateTime;

    private LocalDateTime actualExitTime;

    private LocalDateTime actualEntryTime;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private PassStatus status;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "approved_by_id")
    private User approvedBy;

    private String remarks;

    @Column(nullable = false)
    private LocalDateTime createdAt;

    // Constructors
    public GatePass() {
    }

    public GatePass(Long id, User student, PassType passType, String purpose, String destination, 
                    LocalDateTime departureDateTime, LocalDateTime expectedReturnDateTime, 
                    LocalDateTime actualExitTime, LocalDateTime actualEntryTime, PassStatus status, 
                    User approvedBy, String remarks, LocalDateTime createdAt) {
        this.id = id;
        this.student = student;
        this.passType = passType;
        this.purpose = purpose;
        this.destination = destination;
        this.departureDateTime = departureDateTime;
        this.expectedReturnDateTime = expectedReturnDateTime;
        this.actualExitTime = actualExitTime;
        this.actualEntryTime = actualEntryTime;
        this.status = status;
        this.approvedBy = approvedBy;
        this.remarks = remarks;
        this.createdAt = createdAt;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public User getStudent() {
        return student;
    }

    public void setStudent(User student) {
        this.student = student;
    }

    public PassType getPassType() {
        return passType;
    }

    public void setPassType(PassType passType) {
        this.passType = passType;
    }

    public String getPurpose() {
        return purpose;
    }

    public void setPurpose(String purpose) {
        this.purpose = purpose;
    }

    public String getDestination() {
        return destination;
    }

    public void setDestination(String destination) {
        this.destination = destination;
    }

    public LocalDateTime getDepartureDateTime() {
        return departureDateTime;
    }

    public void setDepartureDateTime(LocalDateTime departureDateTime) {
        this.departureDateTime = departureDateTime;
    }

    public LocalDateTime getExpectedReturnDateTime() {
        return expectedReturnDateTime;
    }

    public void setExpectedReturnDateTime(LocalDateTime expectedReturnDateTime) {
        this.expectedReturnDateTime = expectedReturnDateTime;
    }

    public LocalDateTime getActualExitTime() {
        return actualExitTime;
    }

    public void setActualExitTime(LocalDateTime actualExitTime) {
        this.actualExitTime = actualExitTime;
    }

    public LocalDateTime getActualEntryTime() {
        return actualEntryTime;
    }

    public void setActualEntryTime(LocalDateTime actualEntryTime) {
        this.actualEntryTime = actualEntryTime;
    }

    public PassStatus getStatus() {
        return status;
    }

    public void setStatus(PassStatus status) {
        this.status = status;
    }

    public User getApprovedBy() {
        return approvedBy;
    }

    public void setApprovedBy(User approvedBy) {
        this.approvedBy = approvedBy;
    }

    public String getRemarks() {
        return remarks;
    }

    public void setRemarks(String remarks) {
        this.remarks = remarks;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
