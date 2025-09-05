package com.Project.InventoryManagement.Repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import com.Project.InventoryManagement.Entity.Product;



@Repository
public interface  ProductStockRepo extends JpaRepository<Product, Long> {
    
    @Query(value="""
    SELECT p.id, p.name, p.description, p.type, s.quantity, p.price, s.rating 
    FROM Product p 
    JOIN Stock s ON p.id = s.id
    WHERE p.id = :id
    """, nativeQuery = true)
    Object[] findProductWithStockById(@Param("id") int id);

    @Query(value="""
    SELECT p.id, p.name, p.description, p.type, s.quantity, p.price, s.rating 
    FROM Product p 
    JOIN Stock s ON p.id = s.id
    WHERE p.name = :name"""
    , nativeQuery = true)
    List<Object[]> findProductsWithStockByName(@Param("name") String name);

    @Query(value="""
    SELECT p.id, p.name, p.description, p.type, s.quantity, p.price, s.rating 
    FROM Product p 
    JOIN Stock s ON p.id = s.id
    WHERE p.type = :type"""
    , nativeQuery = true)
    List<Object[]> findProductsWithStockByType(@Param("type") String type);

    @Query(value="""
        SELECT p.id, p.name, p.description, p.type, s.quantity, p.price, s.rating
        FROM Product p
        JOIN Stock s ON p.id = s.id
        WHERE p.name = :name AND p.type = :type
        """, nativeQuery=true)
    List<Object[]> findProductsWithStockByNameAndType(@Param("name") String name, @Param("type") String type);


}
