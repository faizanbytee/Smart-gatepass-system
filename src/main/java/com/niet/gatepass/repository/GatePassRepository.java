package com.niet.gatepass.repository;

import com.niet.gatepass.model.GatePass;
import com.niet.gatepass.model.PassStatus;
import com.niet.gatepass.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface GatePassRepository extends JpaRepository<GatePass, Long> {
    
    List<GatePass> findByStudentOrderByCreatedAtDesc(User student);
    
    List<GatePass> findByStatusOrderByCreatedAtDesc(PassStatus status);
    
    List<GatePass> findByStatusNotOrderByCreatedAtDesc(PassStatus status);
    
    @Query("SELECT g FROM GatePass g WHERE g.student.username = :username AND g.status IN :statuses ORDER BY g.createdAt DESC")
    List<GatePass> findActivePassesByStudentUsername(@Param("username") String username, @Param("statuses") List<PassStatus> statuses);
    
    @Query("SELECT g FROM GatePass g WHERE g.student.username LIKE %:query% OR g.student.name LIKE %:query% ORDER BY g.createdAt DESC")
    List<GatePass> searchPasses(@Param("query") String query);
}
