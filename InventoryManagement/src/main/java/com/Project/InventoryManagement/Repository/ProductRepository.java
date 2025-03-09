package com.Project.InventoryManagement.Repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.Project.InventoryManagement.Entity.Product;

@Repository
public interface ProductRepository extends JpaRepository<Product, Integer>{
    Product findById(int id);
    List<Product> findByProductName(String productName);
    List<Product> findByProductDesc(String productDesc);
    List<Product> findByProductType(String productType);
    List<Product> findBySupplierId(int supplierId);
    List<Product> findByPrice(float price);
    void deleteBySupplierId(int id);
    void deleteByProductName(String name);
}
