package com.Project.InventoryManagement.Repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.Project.InventoryManagement.Entity.Supplier;

@Repository
public interface SupplierRepository extends JpaRepository<Supplier, Integer>{
    List<Supplier> findBySupplierId(int id);
    
    List<Supplier> findBySupplierName(String name);
    List<Supplier> findBySupplierNo(String no);
    List<Supplier> findBySupplierEmail(String email);
    @Transactional
    void deleteBySupplierName(String name);
    @Transactional
    void deleteBySupplierId(int id);
}
