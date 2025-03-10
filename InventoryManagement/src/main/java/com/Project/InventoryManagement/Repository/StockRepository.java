package com.Project.InventoryManagement.Repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import com.Project.InventoryManagement.Entity.Stock;

@Repository
public interface StockRepository extends JpaRepository<Stock, Integer>{
    Stock findById(int id);
    @Query("SELECT s FROM Stock s JOIN Product p ON s.id=p.productId WHERE p.productName=:name")
    List<Stock> findStockByProductName(@Param("name") String name);
    List<Stock> findByRating(String rating);
    List<Stock> findByQuantity(int quantity);
}
