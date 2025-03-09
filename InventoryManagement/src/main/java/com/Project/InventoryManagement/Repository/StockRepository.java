package com.Project.InventoryManagement.Repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.Project.InventoryManagement.Entity.Stock;

@Repository
public interface StockRepository extends JpaRepository<Stock, Integer>{
    Stock findById(int id);
    List<Stock> findByRating(String rating);
    List<Stock> findByQuantity(int quantity);
}
